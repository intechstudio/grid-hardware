#!/usr/bin/env python3
"""
check_design_rules_drift.py — report whether DRC (PCB) and ERC (schematic)
policy has drifted between design folders that are supposed to share the
same manufacturability/correctness rules.

WHY THIS EXISTS: DRC and ERC settings live in each board's .kicad_pro file,
not in a shared location. If one board's constraint thresholds, rule
severities, or waived violations quietly diverge from a sibling board's,
DRC/ERC can pass or fail differently for the same underlying circuit — with
no visible diff anywhere obvious, since .kicad_pro is a large JSON file full
of unrelated editor state (last-used paths, viewport layout, 3D viewer
settings, etc.) that changes on every save regardless.

Scope, deliberately narrow (see the design-rule-storage investigation this
script follows from): of everything KiCad stores under `board.design_settings`
and `erc`, only the keys directly tied to manufacturability/correctness are
checked here — everything else (text/line-width defaults, teardrop settings,
track/via size presets, zone fill style, tuning-pattern cosmetics) is editor
convenience or per-board styling, not policy, and comparing it would just be
noise.

  DRC (`board.design_settings`):
    - `rules`             numeric DRC constraint thresholds (min clearance,
                            min track width, min via size, min hole-to-hole...)
    - `rule_severities`   per-violation-type severity (error/warning/ignore)
    - `drc_exclusions`    specific waived violations

  ERC (`erc`):
    - `rule_severities`   per-violation-type severity, schematic side
    - `pin_map`           the pin-type conflict severity matrix
    - `erc_exclusions`    specific waived violations

Usage:  check_design_rules_drift.py --designs DIR [DIR ...] [--github]

  --designs DIR [DIR ...]   design folders to check (e.g. PCBA-EF44
                              PCBA-BU16). At least 2 required. Each must
                              contain DIR/<basename(DIR)>.kicad_pro (KiCad's
                              own convention: project file name matches its
                              folder name).
  --github                  also emit GitHub Actions error annotations and
                              a run-summary table (auto-enabled when
                              GITHUB_ACTIONS=true). Does not change stdout.

The first design (in the order given) is the baseline; every other design's
settings are compared against it key-by-key (`rules`, both `rule_severities`)
or as a set (`drc_exclusions`/`erc_exclusions`, since exclusion entries are
opaque per-violation strings with no stable order), or by direct equality
with a differing-cell count (`pin_map`, a fixed-size matrix).

Output: a deterministic report on stdout, one block per design pair per
section (DRC, ERC).
Exit status:
  0  every design's DRC and ERC policy matches the baseline
  1  at least one design has real DRC or ERC policy drift
  2  usage / environment error (missing design folder, <2 designs, missing
     or malformed .kicad_pro file)
"""
import argparse
import json
import os
import sys

SECTIONS = [
    {
        "name": "drc",
        "title": "DRC",
        "path": ("board", "design_settings"),
        "dict_keys": ["rules", "rule_severities"],
        "set_keys": ["drc_exclusions"],
        "matrix_keys": [],
    },
    {
        "name": "erc",
        "title": "ERC",
        "path": ("erc",),
        "dict_keys": ["rule_severities"],
        "set_keys": ["erc_exclusions"],
        "matrix_keys": ["pin_map"],
    },
]


def load_project(design_dir):
    pro_path = os.path.join(design_dir, os.path.basename(os.path.normpath(design_dir)) + ".kicad_pro")
    if not os.path.isfile(pro_path):
        return None, pro_path
    with open(pro_path, encoding='utf-8') as f:
        data = json.load(f)
    return data, pro_path


def get_path(data, path):
    node = data
    for key in path:
        node = node.get(key, {})
    return node


def diff_dict(baseline, other):
    """Return a list of (key, baseline_value, other_value) for keys that differ."""
    keys = sorted(set(baseline.keys()) | set(other.keys()))
    return [(k, baseline.get(k, '<missing>'), other.get(k, '<missing>'))
            for k in keys if baseline.get(k, object()) != other.get(k, object())]


def diff_set(baseline, other):
    """A list of opaque per-violation strings; compare as a set."""
    b, o = set(baseline), set(other)
    only_baseline = sorted(b - o)
    only_other = sorted(o - b)
    return only_baseline, only_other


def diff_matrix(baseline, other):
    """A fixed-size matrix (e.g. pin_map); report differing cell count and positions."""
    cells = []
    for r, (brow, orow) in enumerate(zip(baseline, other)):
        for c, (bval, oval) in enumerate(zip(brow, orow)):
            if bval != oval:
                cells.append((r, c, bval, oval))
    if len(baseline) != len(other):
        cells.append(('shape', None, len(baseline), len(other)))
    return cells


def compare_section(section, baseline_data, other_data):
    """Returns dict of key -> finding (or None if that key matches)."""
    baseline_node = get_path(baseline_data, section["path"])
    other_node = get_path(other_data, section["path"])
    findings = {}
    for key in section["dict_keys"]:
        d = diff_dict(baseline_node.get(key, {}), other_node.get(key, {}))
        findings[key] = d if d else None
    for key in section["set_keys"]:
        only_baseline, only_other = diff_set(baseline_node.get(key, []), other_node.get(key, []))
        findings[key] = (only_baseline, only_other) if (only_baseline or only_other) else None
    for key in section["matrix_keys"]:
        cells = diff_matrix(baseline_node.get(key, []), other_node.get(key, []))
        findings[key] = cells if cells else None
    return findings


def all_keys(section):
    return section["dict_keys"] + section["set_keys"] + section["matrix_keys"]


def print_report(section, baseline_dir, other_dir, findings):
    drifted = any(v is not None for v in findings.values())
    status = "DRIFTED" if drifted else "identical"
    print(f"=== [{section['title']}] {other_dir} vs baseline {baseline_dir}: {status} ===")
    for key in all_keys(section):
        finding = findings[key]
        if finding is None:
            print(f"  {key}: match")
            continue
        if key in section["set_keys"]:
            only_baseline, only_other = finding
            for excl in only_baseline:
                print(f"  {key}: only in {baseline_dir}: {excl}")
            for excl in only_other:
                print(f"  {key}: only in {other_dir}: {excl}")
        elif key in section["matrix_keys"]:
            print(f"  {key}: {len(finding)} differing cell(s), e.g. {finding[:5]}")
        else:
            for k, bval, oval in finding:
                print(f"  {key}.{k}: {baseline_dir}={bval!r}  {other_dir}={oval!r}")
    print()
    return drifted


def finding_size(section, key, finding):
    if finding is None:
        return 0
    if key in section["set_keys"]:
        return len(finding[0]) + len(finding[1])
    return len(finding)


def main():
    parser = argparse.ArgumentParser(
        description="Compare DRC (PCB) and ERC (schematic) policy across N design folders.")
    parser.add_argument('--designs', nargs='+', required=True, metavar='DIR',
                         help='Design folders to check (at least 2).')
    parser.add_argument('--github', action='store_true',
                         help='Also emit GitHub Actions error annotations and a run-summary table '
                              '(auto-enabled when GITHUB_ACTIONS=true). Does not change stdout.')
    args = parser.parse_args()
    github_mode = args.github or os.environ.get('GITHUB_ACTIONS') == 'true'

    if len(args.designs) < 2:
        print("error: need at least 2 design folders to compare", file=sys.stderr)
        return 2

    projects = {}
    for d in args.designs:
        if not os.path.isdir(d):
            print(f"error: design folder not found: {d}", file=sys.stderr)
            return 2
        data, pro_path = load_project(d)
        if data is None:
            print(f"error: project file not found: {pro_path}", file=sys.stderr)
            return 2
        projects[d] = data

    baseline_dir = args.designs[0]
    baseline_data = projects[baseline_dir]

    any_drift = False
    # reports: list of (design, section, findings, drifted)
    reports = []
    for d in args.designs[1:]:
        for section in SECTIONS:
            findings = compare_section(section, baseline_data, projects[d])
            drifted = print_report(section, baseline_dir, d, findings)
            reports.append((d, section, findings, drifted))
            any_drift = any_drift or drifted

    if any_drift:
        print("RESULT: DRIFT — one or more designs have DRC or ERC policy that differs from the baseline.")
    else:
        print("RESULT: OK — every design's DRC and ERC policy matches the baseline.")

    if github_mode:
        for d, section, findings, drifted in reports:
            if not drifted:
                continue
            pro_path = os.path.join(d, os.path.basename(os.path.normpath(d)) + ".kicad_pro")
            changed_keys = [k for k in all_keys(section) if findings[k] is not None]
            print(f"::error file={pro_path},title={section['title']} policy drift::{d} {section['title']} policy "
                  f"differs from baseline {baseline_dir} in: {', '.join(changed_keys)}.")
        summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
        if summary_path:
            with open(summary_path, 'a', encoding='utf-8') as f:
                if any_drift:
                    f.write(f"❌ Design rules (DRC+ERC) vs baseline `{baseline_dir}`: drift found\n\n")
                    for section in SECTIONS:
                        keys = all_keys(section)
                        f.write(f"### {section['title']}\n\n")
                        f.write("| Design | " + " | ".join(keys) + " |\n")
                        f.write("| --- | " + " | ".join(["---"] * len(keys)) + " |\n")
                        for d, sec, findings, drifted in reports:
                            if sec is not section:
                                continue
                            cells = ["match" if findings[k] is None else f"DRIFTED ({finding_size(section, k, findings[k])})"
                                     for k in keys]
                            f.write(f"| {d} | " + " | ".join(cells) + " |\n")
                        f.write("\n")
                else:
                    f.write(f"✅ Design rules (DRC+ERC) vs baseline `{baseline_dir}`: all match\n\n")

    return 1 if any_drift else 0


if __name__ == '__main__':
    sys.exit(main())
