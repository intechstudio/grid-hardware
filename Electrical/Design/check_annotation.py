#!/usr/bin/env python3
"""
check_annotation.py — verify that a schematic sheet's reference designators
match what KiCad's own annotator would produce under this repo's fixed
per-sheet-page numbering strategy, without invoking KiCad.

WHY THIS EXISTS: kicad-cli has no `sch annotate` subcommand, and eeschema has
no scripting console (unlike pcbnew) — so there is no headless way to ask
KiCad "reannotate this and show me the diff". Reannotation is GUI-menu-only
(Tools > Annotate Schematic). Instead of driving the GUI, this reimplements
the specific annotation strategy this repo uses and computes what each
symbol's reference *should* be directly, then diffs that against what's
actually saved in the .kicad_sch file.

STRATEGY MODELED — this is exactly KiCad's built-in "First free after sheet
number X 100" numbering option, verified against this project's schematics:
  Scope:      Each sheet *instance* independently (a sheet used more than
              once in the hierarchy — e.g. a filter stage reused per
              channel — is annotated per instance, not per file)
  Order:      Sort symbols by Y position (ties broken by X)
  Numbering:  A sheet instance's page number N (see below) gives it the
              exclusive block N*100+1 .. N*100+99. Each reference prefix
              (R, C, U, J, L, #PWR, #FLG, ...) gets its own counter within
              that block, assigned in Y-then-X sorted order.
  Power/flag symbols (#PWR*, #FLG*, #LOGO*, ...) get exactly one literal
  leading zero prepended to the plain block number (e.g. #PWR0601 for 601,
  #PWR01001 for 1001 — NOT zero-padded to a fixed width); ordinary component
  prefixes are never padded (e.g. R601). Verified against real multi-digit
  page numbers (PCBA-EF44/UI_ENC_FILTER.kicad_sch, pages 8-11).

THE PAGE NUMBER IS THE ONLY INPUT — there is no --start/manual override.
A sheet's page number is not a property of the sheet *file*; it is a
property of the sheet *instance*: the `(sheet ...)` block placed in the
parent schematic carries `(instances (project "NAME" (path "..." (page
"N"))))`. A sheet file used more than once in the hierarchy (e.g.
UI_ENC_FILTER.kicad_sch, placed 4 times inside UI_ENC.kicad_sch for this
repo's EF44 design) gets one independent page number — and therefore one
independent numbering block — per placement. This script walks the full
hierarchy from PROJECT/PROJECT.kicad_sch (root, always page "1"),
recursively following `Sheetfile` properties (the same mechanism KiCad uses
to resolve subsheets) to enumerate every sheet *instance*, each identified by
its full hierarchical path (chain of sheet-instance UUIDs from the root).

A symbol placed on a multiply-instantiated sheet correspondingly carries one
`(path ... (reference "..."))` entry per instance inside its `(instances
(project "NAME" ...))` block, all sharing the same on-page (X, Y) position
(it's the same drawing, reused). Each entry is matched to its owning sheet
instance by exact path equality, and checked independently against that
instance's own page-derived block — see check_sheet_instance().

ENFORCED PROJECT INVARIANTS (KiCad's GUI does not enforce these — this
script does, as a preflight before any per-symbol check runs):
  - every sheet instance's page number is globally unique within the project
  - the root schematic is page 1
  - page numbers are contiguous from 1 with no gaps (i.e. the set of page
    numbers in use is exactly {1, 2, ..., number of sheet instances})
  A violation here is fatal (exit 2): the block-per-page strategy that every
  other check depends on isn't even well-defined until this holds.

A schematic sheet FILE can also be instantiated by more than one PROJECT
(shared sub-sheets — see check_schematic_drift.py); this script only ever
follows and checks the named --project's own instance data.

Usage:  check_annotation.py [--sheet FILE.kicad_sch [FILE.kicad_sch ...]]
                             --project DIR [--github]

  --sheet FILE.kicad_sch   restrict the report to these sheet file(s)
                              (matched by basename; every instance of a
                              matching file is still checked and reported
                              independently). The project-wide preflight
                              (page uniqueness/contiguity, orphan-file
                              detection) always still runs first, since page
                              numbers can only be known by walking the whole
                              hierarchy from the root. If omitted, every
                              reachable, non-root sheet instance is checked.
  --project DIR            the design folder to read (a bare name like
                              "PCBA-EF44" or a path to one, e.g.
                              "Electrical/Design/PCBA-EF44"). Per this repo's
                              convention (folder name == .kicad_pro basename),
                              the KiCad project name matched inside
                              (instances (project "NAME" ...)) blocks — both
                              sheet pages and symbol references — is this
                              directory's basename, not the full DIR string.
  --github                 also emit GitHub Actions error annotations and a
                              run-summary table (auto-enabled when
                              GITHUB_ACTIONS=true). Does not change stdout.

Output: one independently-reported block per sheet INSTANCE (not per file) —
a mismatch table for that instance if any, sorted in the same Y-then-X order
used to compute expected numbers.

Exit status:
  0  every symbol instance's reference matches its modeled block exactly,
     and no orphaned sheet files were found
  1  at least one symbol instance is mis-annotated, and/or an orphaned sheet
     file was found (--sheet omitted only)
  2  usage / environment error, OR a project invariant is violated: broken
     Sheetfile reference, duplicate page number, non-contiguous page
     numbers, root not page 1, unparseable reference
"""
import argparse
import glob
import os
import re
import sys


def find_matching_paren(text, open_index):
    """text[open_index] must be '('. Return the index of its matching ')'."""
    depth = 0
    j = open_index
    n = len(text)
    while j < n:
        if text[j] == '(':
            depth += 1
        elif text[j] == ')':
            depth -= 1
            if depth == 0:
                return j
        j += 1
    return -1


def extract_top_blocks(text, tag):
    """Return the text of every top-level `(tag ...)` block."""
    blocks = []
    for m in re.finditer(r'\n\t\(' + tag + r'\n', text):
        start = m.start() + 1
        depth = 0
        j = start
        n = len(text)
        while j < n:
            if text[j] == '(':
                depth += 1
            elif text[j] == ')':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        blocks.append(text[start:j + 1])
    return blocks


class TreeError(Exception):
    pass


def build_sheet_tree(project_dir, project):
    """Walk the sheet hierarchy from PROJECT/PROJECT.kicad_sch, following
    Sheetfile references, restricted to this project's own instance data.
    Returns a list of instance dicts, each:
      file        basename of the .kicad_sch this instance places
      full_path   this instance's own full hierarchical path (KiCad's path
                    string: root is "/", children append their own uuid)
      page        this project's page number for this instance (str)
    Root is included (file=root, full_path="/", page from its own
    sheet_instances block). Raises TreeError on a broken Sheetfile reference
    (points at a file that doesn't exist) or a missing/unparseable root page.
    """
    root_file = f"{project}.kicad_sch"
    root_path = os.path.join(project_dir, root_file)
    if not os.path.isfile(root_path):
        raise TreeError(f"root sheet not found: {project_dir}/{root_file}")

    with open(root_path, encoding='utf-8') as f:
        root_text = f.read()
    root_page_m = re.search(r'\(sheet_instances\s*\(path "/"\s*\(page "([^"]+)"\)', root_text)
    if not root_page_m:
        raise TreeError(f"{project_dir}/{root_file} has no (sheet_instances (path \"/\" "
                         f"(page ...))) — can't determine the root's own page number")

    # The root's own identifying uuid (its first (uuid "...") tag) is what actually
    # prefixes every descendant's path — the literal "/" above is only used in the
    # root's own self-referential sheet_instances entry, never by its children.
    root_uuid_m = re.search(r'\(uuid "([^"]+)"\)', root_text)
    if not root_uuid_m:
        raise TreeError(f"{project_dir}/{root_file} has no (uuid ...) of its own")

    instances = [{"file": root_file, "full_path": "/", "page": root_page_m.group(1)}]
    stack = [(f"/{root_uuid_m.group(1)}", root_text)]
    while stack:
        full_path, text = stack.pop()
        for block in extract_top_blocks(text, "sheet"):
            file_m = re.search(r'\(property "Sheetfile" "([^"]+)"', block)
            if not file_m:
                continue
            child_file = file_m.group(1)

            # A (sheet ...) block's (instances (project NAME ...)) can carry more than
            # one (path ... (page ...)) pair — one per instantiation of the PARENT sheet
            # (i.e. the file containing this block), when that parent is itself placed
            # more than once in the hierarchy. Pick the one whose path matches the
            # parent instance we're currently walking (full_path), not just the first.
            proj_tag = '(project "' + project + '"'
            proj_idx = block.find(proj_tag)
            if proj_idx == -1:
                continue  # this placement isn't part of OUR project's hierarchy
            proj_close = find_matching_paren(block, proj_idx)
            proj_block = block[proj_idx:proj_close + 1] if proj_close != -1 else block[proj_idx:]
            page_pairs = re.findall(r'\(path "([^"]*)"\s*\(page "([^"]+)"\)', proj_block)
            page = next((p for path, p in page_pairs if path == full_path), None)
            if page is None:
                continue  # no page recorded for this specific parent instance

            uuid_m = re.search(r'\n\t\t\(uuid "([^"]+)"\)', block)
            if not uuid_m:
                raise TreeError(f"a (sheet) block for '{child_file}' under path "
                                 f"'{full_path}' has no (uuid ...)")
            child_full_path = full_path.rstrip('/') + '/' + uuid_m.group(1)

            instances.append({"file": child_file, "full_path": child_full_path,
                               "page": page})

            child_disk_path = os.path.join(project_dir, child_file)
            if not os.path.isfile(child_disk_path):
                raise TreeError(f"broken Sheetfile reference — '{child_file}' is "
                                 f"referenced as a subsheet (under path '{full_path}') "
                                 f"but does not exist in {project_dir}/")
            with open(child_disk_path, encoding='utf-8') as f:
                child_text = f.read()
            stack.append((child_full_path, child_text))

    return instances


def validate_pages(instances):
    """Check the enforced invariants over a project's sheet-instance list.
    Returns a list of human-readable problem strings (empty if all OK)."""
    problems = []
    root = next((i for i in instances if i["full_path"] == "/"), None)
    if root is None or root["page"] != "1":
        problems.append(f"root sheet must be page 1, found "
                         f"'{root['page'] if root else '?'}'")

    pages = []
    for inst in instances:
        try:
            pages.append(int(inst["page"]))
        except ValueError:
            problems.append(f"sheet instance '{inst['file']}' at path "
                             f"'{inst['full_path']}' has a non-integer page "
                             f"'{inst['page']}'")

    from collections import Counter
    counts = Counter(pages)
    dupes = sorted(p for p, c in counts.items() if c > 1)
    for p in dupes:
        owners = [i for i in instances if i["page"].isdigit() and int(i["page"]) == p]
        owner_desc = ", ".join(f"{i['file']} ({i['full_path']})" for i in owners)
        problems.append(f"page {p} is used by {len(owners)} sheet instances "
                         f"(must be unique): {owner_desc}")

    if pages:
        expected = set(range(1, len(pages) + 1))
        missing = sorted(expected - set(pages))
        if missing:
            problems.append(f"page numbers are not contiguous from 1 — missing: "
                             f"{', '.join(str(p) for p in missing)}")

    return problems


PREFIX_RE = re.compile(r'^(#?[A-Za-z]+)(\d+)$')


def parse_symbols(text, project):
    """Return list of dicts: uuid, x, y, prefix, path, actual_ref,
    actual_num — one per (symbol, instance-path) pair for this project. A
    symbol not instantiated by PROJECT at all contributes nothing."""
    symbols = []
    for block in extract_top_blocks(text, "symbol"):
        uuid_m = re.search(r'\(uuid "([^"]*)"\)', block)
        if not uuid_m:
            continue
        uuid = uuid_m.group(1)

        proj_tag = '(project "' + project + '"'
        idx = block.find(proj_tag)
        if idx == -1:
            continue
        close = find_matching_paren(block, idx)
        proj_block = block[idx:close + 1] if close != -1 else block[idx:]
        pairs = re.findall(r'\(path "([^"]*)"\s*\(reference "([^"]*)"\)', proj_block)
        if not pairs:
            continue

        at_m = re.search(r'\(at ([\-\d.]+) ([\-\d.]+)', block)
        if not at_m:
            raise ValueError(f"symbol {uuid} has no (at X Y) position")
        x, y = float(at_m.group(1)), float(at_m.group(2))

        for path, ref in pairs:
            m = PREFIX_RE.match(ref)
            if not m:
                raise ValueError(f"symbol {uuid}: reference '{ref}' doesn't "
                                  f"match <prefix><digits>")
            prefix, num_str = m.group(1), m.group(2)
            symbols.append({
                "uuid": uuid, "x": x, "y": y, "prefix": prefix, "path": path,
                "actual_ref": ref, "actual_num": int(num_str),
            })
    return symbols


def compute_ranks(symbols):
    """Assign each symbol dict a "rank" (in place): its 1-based position
    within its prefix group when sorted Y-then-X. Symbols sharing (prefix,
    uuid) across different instance paths all share the same rank, since
    they're the same physical symbol at the same drawn position — the rank
    only needs computing once per unique (uuid, prefix)."""
    by_uuid = {}
    for s in symbols:
        by_uuid[s["uuid"]] = s  # position/prefix are instance-independent

    by_prefix = {}
    for s in by_uuid.values():
        by_prefix.setdefault(s["prefix"], []).append(s)

    rank_of_uuid = {}
    for prefix, group in by_prefix.items():
        group.sort(key=lambda s: (s["y"], s["x"]))
        for i, s in enumerate(group, start=1):
            rank_of_uuid[s["uuid"]] = i

    for s in symbols:
        s["rank"] = rank_of_uuid[s["uuid"]]


def expected_ref(prefix, page, rank):
    """Power/flag/logo symbols (# prefix) get exactly one literal leading
    zero prepended to the plain decimal number — NOT zero-padded to a fixed
    width. For a 3-digit block number (single-digit page, e.g. 801) that
    looks identical to %04d (-> "0801"), but for a 4-digit block number
    (double-digit page, e.g. 1001) KiCad still prepends only one zero
    (-> "01001", five digits) rather than none. Verified against
    PCBA-EF44/UI_ENC_FILTER.kicad_sch instances on pages 8-11. Ordinary
    component prefixes are never padded (e.g. R601)."""
    num = page * 100 + rank
    return f"{prefix}0{num}" if prefix.startswith('#') else f"{prefix}{num}"


def print_table(rows):
    width_ref = max(max(len(r["actual_ref"]) for r in rows), len("ACTUAL"))
    width_exp = max(max(len(r["expected_ref"]) for r in rows), len("EXPECTED"))
    print(f"{'UUID':<38} {'POSITION':<16} {'ACTUAL':<{width_ref}} {'EXPECTED':<{width_exp}}")
    print(f"{'-'*38} {'-'*16} {'-'*width_ref} {'-'*width_exp}")
    for r in sorted(rows, key=lambda s: (s["y"], s["x"])):
        pos = f"({r['x']:g}, {r['y']:g})"
        print(f"{r['uuid']:<38} {pos:<16} {r['actual_ref']:<{width_ref}} {r['expected_ref']:<{width_exp}}")


def emit_github_annotations(sheet_file, mismatches):
    for r in mismatches:
        print(f"::error file={sheet_file},title=Annotation mismatch::"
              f"symbol {r['uuid']} at ({r['x']:g}, {r['y']:g}) is annotated "
              f"'{r['actual_ref']}', expected '{r['expected_ref']}' under the "
              f"modeled annotation strategy.")


def check_sheet_instance(project_dir, inst, project, github_mode):
    """Check one sheet instance. Returns (code, report):
      code    0 (OK), 1 (misannotated), 2 (usage error), or None (skipped —
                no components of PROJECT on this instance)
      report  dict for the GitHub summary table: file, page, path, status,
                symbol_count, mismatch_count (None if code == 2)
    """
    sheet_path = os.path.join(project_dir, inst["file"])
    with open(sheet_path, encoding='utf-8') as f:
        text = f.read()

    try:
        all_symbols = parse_symbols(text, project)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2, None

    compute_ranks(all_symbols)
    symbols = [s for s in all_symbols if s["path"] == inst["full_path"]]

    label = f"{inst['file']} — page {inst['page']} (path {inst['full_path']})"
    if not symbols:
        print(f"=== {label} ===")
        print("SKIPPED — no components of this project on this instance.\n")
        report = {"file": inst["file"], "page": inst["page"], "path": inst["full_path"],
                   "status": "SKIPPED", "symbol_count": 0, "mismatch_count": 0}
        return None, report

    page = int(inst["page"])
    for s in symbols:
        s["expected_ref"] = expected_ref(s["prefix"], page, s["rank"])
    mismatches = [s for s in symbols if s["actual_ref"] != s["expected_ref"]]

    print(f"=== {label} ===")
    print(f"{len(symbols)} symbols checked, {len(mismatches)} mismatched\n")
    if mismatches:
        print_table(mismatches)
        print()
        print("RESULT: MISANNOTATED — one or more references don't match the "
              "modeled annotation strategy.")
        if github_mode:
            emit_github_annotations(sheet_path, mismatches)
        report = {"file": inst["file"], "page": inst["page"], "path": inst["full_path"],
                   "status": "MISANNOTATED", "symbol_count": len(symbols),
                   "mismatch_count": len(mismatches)}
        return 1, report

    print("RESULT: OK — every reference matches the modeled annotation strategy.")
    report = {"file": inst["file"], "page": inst["page"], "path": inst["full_path"],
               "status": "OK", "symbol_count": len(symbols), "mismatch_count": 0}
    return 0, report


def write_github_summary(project, preflight_error, orphans, reports, any_finding):
    summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
    if not summary_path:
        return
    with open(summary_path, 'a', encoding='utf-8') as f:
        f.write("## Annotation gate\n\n")
        if preflight_error:
            f.write(f"❌ **PREFLIGHT FAILED** — {preflight_error}\n\n")
            return
        if any_finding:
            extra = " and orphaned sheet(s) were found" if orphans else ""
            f.write(f"❌ **MISANNOTATED** — one or more sheet instances don't match "
                    f"the modeled annotation strategy{extra}.\n\n")
        else:
            f.write("✅ **OK** — every checked sheet instance matches the modeled "
                    "annotation strategy.\n\n")
        if orphans:
            f.write(f"**Orphaned sheets** (present in `{project}/` but not reachable "
                    f"from the root): " + ", ".join(f"`{o}`" for o in orphans) + "\n\n")
        if reports:
            f.write("| Sheet | Page | Status | Symbols | Mismatched |\n")
            f.write("| --- | ---: | --- | ---: | ---: |\n")
            for r in reports:
                f.write(f"| {r['file']} | {r['page']} | {r['status']} | "
                         f"{r['symbol_count']} | {r['mismatch_count']} |\n")
            f.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description="Check schematic sheet instances' reference designators "
                    "against this repo's page-number-driven annotation strategy.")
    parser.add_argument('--sheet', nargs='+', dest='sheets', default=None,
                         metavar='FILE.kicad_sch',
                         help='Restrict the report to these sheet file(s) (matched by '
                              'basename; every instance of a matching file is still '
                              'checked independently). The project-wide preflight always '
                              'runs first regardless. If omitted, every reachable, '
                              'non-root sheet instance is checked.')
    parser.add_argument('--project', required=True, metavar='DIR',
                         help='Design folder to read (bare name or a path to one, e.g. '
                              '"Electrical/Design/PCBA-EF44"). The KiCad project name '
                              'matched inside (instances (project "NAME" ...)) blocks is '
                              'this directory\'s basename.')
    parser.add_argument('--github', action='store_true',
                         help='Also emit GitHub Actions error annotations and a '
                              'run-summary table (auto-enabled when GITHUB_ACTIONS=true). '
                              'Does not change stdout.')
    args = parser.parse_args()
    github_mode = args.github or os.environ.get('GITHUB_ACTIONS') == 'true'

    # --project is a directory (bare name or a path to one, e.g. "PCBA-EF44" or
    # "Electrical/Design/PCBA-EF44") to read files from. The KiCad PROJECT NAME
    # matched inside (instances (project "NAME" ...)) blocks is that directory's
    # basename, per this repo's convention (folder name == .kicad_pro basename)
    # already relied on throughout this script — the two are NOT the same string
    # whenever --project includes a path.
    project_dir = args.project
    project_name = os.path.basename(os.path.normpath(args.project))
    root_sheet_path = os.path.join(project_dir, f"{project_name}.kicad_sch")

    if not os.path.isdir(project_dir):
        print(f"error: project folder not found: {project_dir}", file=sys.stderr)
        return 2

    print(f"=== Preflight: sheet hierarchy for {project_dir} ===")
    try:
        instances = build_sheet_tree(project_dir, project_name)
    except TreeError as e:
        print(f"error: {e}", file=sys.stderr)
        if github_mode:
            print(f"::error file={root_sheet_path},title=Sheet hierarchy error::{e}")
            write_github_summary(project_dir, str(e), [], [], True)
        return 2

    problems = validate_pages(instances)
    if problems:
        for p in problems:
            print(f"error: {p}", file=sys.stderr)
        if github_mode:
            for p in problems:
                print(f"::error file={root_sheet_path},title=Page numbering error::{p}")
            write_github_summary(project_dir, "; ".join(problems), [], [], True)
        return 2
    print(f"OK — {len(instances)} sheet instance(s), page numbers unique and "
          f"contiguous from 1.")

    worst = 0
    present = {os.path.basename(p)
               for p in glob.glob(os.path.join(project_dir, "*.kicad_sch"))}
    reachable_files = {inst["file"] for inst in instances}
    orphans = sorted(present - reachable_files)
    if args.sheets is None:
        if orphans:
            print(f"{len(orphans)} orphaned sheet(s) found — present in {project_dir}/ "
                  f"but not reachable from the root sheet:")
            for f in orphans:
                print(f"  {f}")
            worst = max(worst, 1)
            if github_mode:
                for o in orphans:
                    print(f"::error file={os.path.join(project_dir, o)},"
                          f"title=Orphaned sheet::'{o}' is present in {project_dir}/ but "
                          f"not reachable from the root sheet — it isn't wired into the "
                          f"design hierarchy.")
        else:
            print("OK — every *.kicad_sch in the folder is reachable from the root sheet.")
    print()

    non_root = [i for i in instances if i["full_path"] != "/"]
    if args.sheets is not None:
        wanted = set(args.sheets)
        non_root = [i for i in non_root if i["file"] in wanted]
        if not non_root:
            print(f"error: none of the given --sheet file(s) are reachable instances "
                  f"in {project_dir}/", file=sys.stderr)
            return 2

    non_root.sort(key=lambda i: (i["file"], int(i["page"]) if i["page"].isdigit() else 0))
    print(f"checking {len(non_root)} sheet instance(s) in {project_dir}/\n")

    reports = []
    for i, inst in enumerate(non_root):
        if i > 0:
            print()
        code, report = check_sheet_instance(project_dir, inst, project_name, github_mode)
        if report is not None:
            reports.append(report)
        if code is None:
            continue
        if code == 2:
            if github_mode:
                write_github_summary(project_dir, None, orphans, reports, True)
            return 2
        worst = max(worst, code)

    if github_mode:
        write_github_summary(project_dir, None, orphans, reports, worst > 0)

    return worst


if __name__ == '__main__':
    sys.exit(main())
