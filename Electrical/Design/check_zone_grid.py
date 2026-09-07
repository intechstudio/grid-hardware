#!/usr/bin/env python3
"""
check_zone_grid.py — verify that every copper zone's outline vertices in a
board's .kicad_pcb sit exactly on a fixed raster.

WHY THIS EXISTS: PCBA-PO16, PCBA-BU16, and PCBA-EF44 all carry the same
handful of copper-pour zones (+5V/+3V3/GND fills), copy-pasted between
designs the same way the shared schematic sheets are. Inspecting them
turned up a few outline vertices with sub-micron floating-point drift
(e.g. 55.996533 instead of 56, 50.003467 instead of 50) — harmless to DRC,
but a sign the same zone outline had been nudged independently by a mouse
drag or an editor round-trip in at least one of the three copies, rather
than staying pixel-identical the way the shared sheets are checked to.
There was no automated check that would have caught this drift, so it sat
unnoticed across all three boards until found by hand. This script closes
that gap: an absolute (non-comparative) check, same category as
check_annotation.py, run per design rather than against a baseline.

Only the zone's own outline — the `(polygon (pts ...))` the user actually
draws/edits — is checked. The `(filled_polygon ...)` KiCad computes from
that outline is derived, regenerated on every zone refill, and deliberately
ignored here.

Usage:  check_zone_grid.py --project DIR [--raster MM] [--github]

  --project DIR   design folder containing DIR/DIR.kicad_pcb (e.g.
                    Electrical/Design/PCBA-PO16)
  --raster MM     required grid, in mm (default: 1.0 — the finest grid
                    every zone outline in this repo currently satisfies
                    exactly; tighten only once every design's outlines
                    actually sit on the tighter grid)
  --github        also emit GitHub Actions error annotations (auto-enabled
                    when GITHUB_ACTIONS=true). Does not change stdout.

Output: one line per off-grid vertex, then a summary.
Exit status:
  0  every zone outline vertex lands exactly on the raster (tolerance 1e-6mm)
  1  at least one vertex is off-grid
  2  usage / environment error (missing project dir or .kicad_pcb, or the
       file has no zones at all)
"""
import argparse
import os
import re
import sys

TOLERANCE = 1e-6


def find_zone_blocks(text):
    """Return the raw text of every top-level `(zone ...)` block."""
    blocks = []
    for m in re.finditer(r'\n\t\(zone\n', text):
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


def zone_outline_points(block):
    """Return the list of (x, y) float pairs in this zone's own outline
    polygon (the first `(polygon (pts ...))`, before any `filled_polygon`)."""
    fill_idx = block.find('(filled_polygon')
    head = block[:fill_idx] if fill_idx != -1 else block
    poly_m = re.search(r'\(polygon\s*\(pts(.*?)\)\s*\)\s*\)', head, re.S)
    if not poly_m:
        return []
    return [(float(x), float(y))
            for x, y in re.findall(r'\(xy ([\-\d.]+) ([\-\d.]+)\)', poly_m.group(1))]


def off_grid(value, raster):
    remainder = value % raster
    return min(remainder, raster - remainder) > TOLERANCE


def check_project(project_dir, raster, github_mode):
    project = os.path.basename(os.path.normpath(project_dir))
    pcb_path = os.path.join(project_dir, f"{project}.kicad_pcb")
    if not os.path.isfile(pcb_path):
        print(f"ERROR: {pcb_path} not found", file=sys.stderr)
        return 2

    with open(pcb_path, encoding='utf-8') as f:
        text = f.read()

    zones = find_zone_blocks(text)
    if not zones:
        print(f"ERROR: no (zone ...) blocks found in {pcb_path}", file=sys.stderr)
        return 2

    any_off = False
    for block in zones:
        net_m = re.search(r'\(net "([^"]*)"\)', block)
        layer_m = re.search(r'\(layer "([^"]+)"\)', block)
        net = net_m.group(1) if net_m else "?"
        layer = layer_m.group(1) if layer_m else "?"
        pts = zone_outline_points(block)
        bad = [(x, y) for x, y in pts if off_grid(x, raster) or off_grid(y, raster)]
        if not bad:
            print(f"=== zone net={net!r} layer={layer} — {len(pts)} vertices, "
                  f"all on {raster}mm grid ===")
            continue
        any_off = True
        print(f"=== zone net={net!r} layer={layer} — {len(bad)}/{len(pts)} "
              f"vertices OFF the {raster}mm grid ===")
        for x, y in bad:
            print(f"    ({x}, {y})")
            if github_mode:
                print(f"::error file={pcb_path},title=Zone outline off grid::"
                      f"zone net={net} layer={layer} vertex ({x}, {y}) is not "
                      f"on the {raster}mm raster")

    print()
    if any_off:
        print(f"RESULT: MISALIGNED — one or more zone outlines are off the "
              f"{raster}mm grid.")
        return 1
    print(f"RESULT: OK — every zone outline vertex is on the {raster}mm grid.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Verify copper zone outlines sit on a fixed grid.")
    parser.add_argument('--project', required=True, metavar='DIR',
                         help='design folder containing DIR/DIR.kicad_pcb')
    parser.add_argument('--raster', type=float, default=1.0, metavar='MM',
                         help='required grid in mm (default: 1.0)')
    parser.add_argument('--github', action='store_true',
                         help='also emit GitHub Actions error annotations '
                              '(auto-enabled when GITHUB_ACTIONS=true)')
    args = parser.parse_args()
    github_mode = args.github or os.environ.get('GITHUB_ACTIONS') == 'true'

    return check_project(args.project, args.raster, github_mode)


if __name__ == '__main__':
    sys.exit(main())
