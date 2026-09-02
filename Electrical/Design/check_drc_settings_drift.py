#!/usr/bin/env python3
"""
check_drc_settings_drift.py — report whether DRC policy has drifted between
design folders that are supposed to share the same manufacturability rules.

WHY THIS EXISTS: DRC (Design Rule Check) settings live in each board's
.kicad_pro file, not in a shared location. If one board's minimum clearance,
rule severities, or waived violations quietly diverge from a sibling board's,
DRC can pass or fail differently for the same underlying manufacturing
capability — with no visible diff anywhere obvious, since .kicad_pro is a
large JSON file full of unrelated editor state (last-used paths, viewport
layout, 3D viewer settings, etc.) that changes on every save regardless.

Scope, deliberately narrow: of everything KiCad stores under
`board.design_settings` (see the DRC-storage investigation this script
follows from), only three keys are directly tied to board manufacturability
and are checked here:
  - `rules`             the numeric DRC constraint thresholds (min clearance,
                          min track width, min via size, min hole-to-hole...)
  - `rule_severities`   per-violation-type severity (error/warning/ignore) —
                          silently downgrading one to "ignore" on one board
                          changes what DRC actually catches there
  - `drc_exclusions`    specific waived violations

Everything else in `design_settings` (text/line-width defaults, teardrop
settings, track/via size presets, zone fill style, tuning-pattern cosmetics)
is left alone: it's editor convenience or per-board styling, not
manufacturability policy, and comparing it would just be noise.

Usage:  check_drc_settings_drift.py --designs DIR [DIR ...] [--github]

  --designs DIR [DIR ...]   design folders to check (e.g. PCBA-EF44
                              PCBA-BU16). At least 2 required. Each must
                              contain DIR/<basename(DIR)>.kicad_pro (KiCad's
                              own convention: project file name matches its
                              folder name).
  --github                  also emit GitHub Actions error annotations and
                              a run-summary table (auto-enabled when
                              GITHUB_ACTIONS=true). Does not change stdout.

The first design (in the order given) is the baseline; every other design's
three settings blocks are compared against it key-by-key (rules,
rule_severities) or as a set (drc_exclusions, since exclusion entries are
typically opaque per-violation strings with no stable order).

Output: a deterministic report on stdout, one table per design pair.
Exit status:
  0  every design's DRC policy matches the baseline
  1  at least one design has real DRC-policy drift
  2  usage / environment error (missing design folder, <2 designs, missing
     or malformed .kicad_pro file)
"""
import argparse
import json
import os
import sys

CHECKED_KEYS = ["rules", "rule_severities", "drc_exclusions"]


def load_design_settings(design_dir):
    pro_path = os.path.join(design_dir, os.path.basename(os.path.normpath(design_dir)) + ".kicad_pro")
    if not os.path.isfile(pro_path):
        return None, pro_path
    with open(pro_path, encoding='utf-8') as f:
        data = json.load(f)
    ds = data.get('board', {}).get('design_settings', {})
    return ds, pro_path


def diff_dict(baseline, other):
    """Return a list of (key, baseline_value, other_value) for keys that differ."""
    keys = sorted(set(baseline.keys()) | set(other.keys()))
    return [(k, baseline.get(k, '<missing>'), other.get(k, '<missing>'))
            for k in keys if baseline.get(k, object()) != other.get(k, object())]


def diff_exclusions(baseline, other):
    """drc_exclusions is a list of opaque per-violation strings; compare as a set."""
    b, o = set(baseline), set(other)
    only_baseline = sorted(b - o)
    only_other = sorted(o - b)
    return only_baseline, only_other


def compare(baseline_ds, other_ds):
    """Returns dict of key -> finding (or None if that key matches)."""
    findings = {}
    for key in ("rules", "rule_severities"):
        d = diff_dict(baseline_ds.get(key, {}), other_ds.get(key, {}))
        findings[key] = d if d else None
    only_baseline, only_other = diff_exclusions(
        baseline_ds.get("drc_exclusions", []), other_ds.get("drc_exclusions", []))
    findings["drc_exclusions"] = (only_baseline, only_other) if (only_baseline or only_other) else None
    return findings


def print_report(baseline_dir, other_dir, findings):
    drifted = any(v is not None for v in findings.values())
    status = "DRIFTED" if drifted else "identical"
    print(f"=== {other_dir} vs baseline {baseline_dir}: {status} ===")
    for key in CHECKED_KEYS:
        finding = findings[key]
        if finding is None:
            print(f"  {key}: match")
            continue
        if key == "drc_exclusions":
            only_baseline, only_other = finding
            for excl in only_baseline:
                print(f"  {key}: only in {baseline_dir}: {excl}")
            for excl in only_other:
                print(f"  {key}: only in {other_dir}: {excl}")
        else:
            for k, bval, oval in finding:
                print(f"  {key}.{k}: {baseline_dir}={bval!r}  {other_dir}={oval!r}")
    print()
    return drifted


def main():
    parser = argparse.ArgumentParser(
        description="Compare DRC policy (rules, rule_severities, drc_exclusions) across N design folders.")
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

    settings = {}
    for d in args.designs:
        if not os.path.isdir(d):
            print(f"error: design folder not found: {d}", file=sys.stderr)
            return 2
        ds, pro_path = load_design_settings(d)
        if ds is None:
            print(f"error: project file not found: {pro_path}", file=sys.stderr)
            return 2
        settings[d] = ds

    baseline_dir = args.designs[0]
    baseline_ds = settings[baseline_dir]

    any_drift = False
    reports = []
    for d in args.designs[1:]:
        findings = compare(baseline_ds, settings[d])
        drifted = print_report(baseline_dir, d, findings)
        reports.append((d, findings, drifted))
        any_drift = any_drift or drifted

    if any_drift:
        print("RESULT: DRIFT — one or more designs have DRC policy that differs from the baseline.")
    else:
        print("RESULT: OK — every design's DRC policy (rules, rule_severities, drc_exclusions) matches the baseline.")

    if github_mode:
        for d, findings, drifted in reports:
            if not drifted:
                continue
            pro_path = os.path.join(d, os.path.basename(os.path.normpath(d)) + ".kicad_pro")
            changed_keys = [k for k in CHECKED_KEYS if findings[k] is not None]
            print(f"::error file={pro_path},title=DRC policy drift::{d} DRC policy differs from baseline "
                  f"{baseline_dir} in: {', '.join(changed_keys)}.")
        summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
        if summary_path:
            with open(summary_path, 'a', encoding='utf-8') as f:
                f.write("## DRC policy drift gate\n\n")
                if any_drift:
                    f.write("❌ **DRIFT** — one or more designs have DRC policy that differs from the baseline.\n\n")
                else:
                    f.write("✅ **OK** — every design's DRC policy matches the baseline.\n\n")
                f.write(f"Baseline: `{baseline_dir}`\n\n")
                f.write("| Design | rules | rule_severities | drc_exclusions |\n")
                f.write("| --- | --- | --- | --- |\n")
                for d, findings, drifted in reports:
                    cells = ["match" if findings[k] is None else f"DRIFTED ({len(findings[k]) if k != 'drc_exclusions' else len(findings[k][0]) + len(findings[k][1])})"
                             for k in CHECKED_KEYS]
                    f.write(f"| {d} | {cells[0]} | {cells[1]} | {cells[2]} |\n")

    return 1 if any_drift else 0


if __name__ == '__main__':
    sys.exit(main())
