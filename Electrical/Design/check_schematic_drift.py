#!/usr/bin/env python3
"""
check_schematic_drift.py — report whether the same-named KiCad sub-sheet,
duplicated across N design folders, has actually drifted apart.

WHY THIS EXISTS: some hierarchical sheets (e.g. USB_POWER.kicad_sch,
GRID.kicad_sch) are duplicated verbatim into more than one PCBA-*/FP-*
project directory instead of living in one shared location. That's fine as
long as the copies stay in sync, but nothing currently catches it when they
don't. KiCad also rewrites a few fields purely as a side effect of which
project last had a shared-origin file open (see below), which makes a plain
`diff` noisy even between two copies that are otherwise byte-for-byte the
same circuit. This script filters that expected noise out before comparing,
so what's left in the report is real drift: added/removed/moved components,
changed values, rewired nets.

Normalized (ignored) per-copy noise, matching how KiCad annotates a sheet
that's instantiated by more than one project:
  - `(project "NAME" ...)`      the owning project's name inside an
                                 `(instances ...)` block
  - `(reference "R601")`        a project's own reference designator for one
                                 symbol instance, inside `(instances ...)`
  - `property "Reference" "R601"`  the symbol's cached top-level reference,
                                 which KiCad rewrites to match whichever
                                 project most recently had the file open
  - `(page "7")`                 a project's own page number for a nested
                                 sub-sheet
  - CRLF vs LF line endings

Everything else — UUIDs included — must match. A UUID mismatch on what
should be the same component is itself a real finding (it means the parts
were placed independently, not derived from a shared origin), not noise.

Usage:  check_schematic_drift.py --designs DIR [DIR ...]
                                  --sheets NAME [NAME ...]
                                  [--diff-out DIR] [--github]

  --designs DIR [DIR ...]   design folders to check (e.g. PCBA-EF44
                              PCBA-BU16 PCBA-KB25). At least 2 required.
  --sheets NAME [NAME ...]  sub-sheet base name(s) to check in each design
                              folder, with or without the .kicad_sch
                              extension (e.g. USB_POWER GRID). At least 1
                              required.

  For each sheet name, this looks for DIR/NAME.kicad_sch under every listed
  design folder. A design that doesn't have that file is reported as
  "missing" (not a failure on its own — not every design needs every
  sheet). The first design (in the order given) that DOES have the file
  becomes the baseline for that sheet; every other design's copy is
  normalized and compared against it.

  --diff-out DIR   write the full unified diff for each drifted copy to
                    DIR/<sheet>/<design>.diff (baseline noise-stripped too,
                    so the diff shows only real content changes)
  --github         also emit GitHub Actions error annotations and a
                    run-summary table (auto-enabled when
                    GITHUB_ACTIONS=true). Does not change stdout.

Output: a deterministic report on stdout, one table per sheet.
Exit status:
  0  every existing copy of every sheet matches its baseline
  1  at least one sheet has a real drifted copy
  2  usage / environment error (missing design folder, <2 designs, no
     sheets given, or a sheet has zero copies across all designs)
"""
import argparse
import difflib
import os
import re
import sys

NOISE_PATTERNS = [
    (re.compile(r'\(project "[^"]*"'), '(project "PROJECT"'),
    (re.compile(r'\(reference "[^"]*"\)'), '(reference "REF")'),
    (re.compile(r'property "Reference" "[^"]*"'), 'property "Reference" "REF"'),
    (re.compile(r'\(page "[^"]*"\)'), '(page "N")'),
]


def normalize(text):
    text = text.replace('\r\n', '\n')
    for pattern, replacement in NOISE_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def load(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def check_sheet(sheet, designs, diff_out):
    """Compare one sheet's copies across all designs, in --designs order.
    Returns (rows, drifted, existing_count)."""
    candidates = [(d, os.path.join(d, f"{sheet}.kicad_sch")) for d in designs]
    existing = [(d, p) for d, p in candidates if os.path.isfile(p)]
    if not existing:
        return [], False, 0

    baseline_path = existing[0][1]
    baseline_norm = normalize(load(baseline_path))

    rows = []
    drifted = False
    for d, p in candidates:
        if not os.path.isfile(p):
            rows.append((p, "missing", ""))
            continue
        if p == baseline_path:
            rows.append((p, "baseline", ""))
            continue
        norm = normalize(load(p))
        if norm == baseline_norm:
            rows.append((p, "identical", ""))
            continue
        diff_lines = list(difflib.unified_diff(
            baseline_norm.splitlines(), norm.splitlines(),
            fromfile=baseline_path, tofile=p, lineterm=''))
        changed = sum(1 for line in diff_lines if line.startswith(('+', '-'))
                      and not line.startswith(('+++', '---')))
        rows.append((p, "DRIFTED", changed))
        drifted = True
        if diff_out:
            sheet_dir = os.path.join(diff_out, sheet)
            os.makedirs(sheet_dir, exist_ok=True)
            safe_name = d.rstrip(os.sep).replace(os.sep, '_')
            out_path = os.path.join(sheet_dir, f"{safe_name}.diff")
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(diff_lines) + '\n')

    return rows, drifted, len(existing)


def print_table(sheet, rows):
    print(f"=== {sheet} ===")
    width = max((len(r[0]) for r in rows), default=0)
    width = max(width, len("FILE"))
    print(f"{'FILE':<{width}}  {'STATUS':<10} {'CHANGED LINES':>13}")
    print(f"{'-'*width}  {'-'*10} {'-'*13}")
    for path, status, changed in rows:
        changed_str = str(changed) if status == "DRIFTED" else ""
        print(f"{path:<{width}}  {status:<10} {changed_str:>13}")
    print()


def emit_github_annotations(results):
    for sheet, rows in results:
        for path, status, changed in rows:
            if status != "DRIFTED":
                continue
            print(f"::error file={path},title=Schematic drift::{sheet} — {path} DRIFTED from baseline "
                  f"({changed} changed lines). Duplicated sheets must stay in sync, or the difference "
                  f"must be intentional.")


def write_github_summary(results, any_drift):
    summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
    if not summary_path:
        return
    with open(summary_path, 'a', encoding='utf-8') as f:
        f.write("## Schematic drift gate\n\n")
        if any_drift:
            f.write("❌ **DRIFT** — one or more sheet copies differ from their baseline beyond expected per-project annotation noise.\n\n")
        else:
            f.write("✅ **OK** — every sheet's copies match their baseline (ignoring per-project annotation noise).\n\n")
        for sheet, rows in results:
            f.write(f"### {sheet}\n\n")
            f.write("| File | Status | Changed lines |\n")
            f.write("| --- | --- | ---: |\n")
            for path, status, changed in rows:
                changed_str = str(changed) if status == "DRIFTED" else ""
                f.write(f"| {path} | {status} | {changed_str} |\n")
            f.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description="Compare a named sub-sheet's copies across N design folders for real (non-annotation) drift.")
    parser.add_argument('--designs', nargs='+', required=True, metavar='DIR',
                         help='Design folders to check (at least 2).')
    parser.add_argument('--sheets', nargs='+', required=True, metavar='NAME',
                         help='Sub-sheet base name(s) to check, with or without .kicad_sch.')
    parser.add_argument('--diff-out', metavar='DIR',
                         help='Directory to write full unified diffs for drifted copies (DIR/<sheet>/<design>.diff).')
    parser.add_argument('--github', action='store_true',
                         help='Also emit GitHub Actions error annotations and a run-summary table '
                              '(auto-enabled when GITHUB_ACTIONS=true). Does not change stdout.')
    args = parser.parse_args()
    github_mode = args.github or os.environ.get('GITHUB_ACTIONS') == 'true'

    if len(args.designs) < 2:
        print("error: need at least 2 design folders to compare", file=sys.stderr)
        return 2

    for d in args.designs:
        if not os.path.isdir(d):
            print(f"error: design folder not found: {d}", file=sys.stderr)
            return 2

    sheets = [s[:-len('.kicad_sch')] if s.endswith('.kicad_sch') else s for s in args.sheets]

    results = []
    any_drift = False
    for sheet in sheets:
        rows, drifted, n_existing = check_sheet(sheet, args.designs, args.diff_out)
        if n_existing == 0:
            print(f"error: sheet '{sheet}.kicad_sch' not found in any design folder", file=sys.stderr)
            return 2
        print_table(sheet, rows)
        results.append((sheet, rows))
        any_drift = any_drift or drifted

    if any_drift:
        print("RESULT: DRIFT — one or more sheet copies differ from their baseline beyond expected per-project annotation noise.")
        if args.diff_out:
            print(f"Full diffs written under {args.diff_out}/")
    else:
        print("RESULT: OK — every sheet's copies match their baseline (ignoring per-project annotation noise).")

    if github_mode:
        emit_github_annotations(results)
        write_github_summary(results, any_drift)

    return 1 if any_drift else 0


if __name__ == '__main__':
    sys.exit(main())
