#!/usr/bin/env bash
#
# check_silkscreen.sh — fail if any KiCad design has an empty silkscreen layer.
#
# WHY THIS EXISTS: when the PCB manufacturer receives gerbers with an empty
# layer they suspect a gerber-export fault, halt, and ask questions — delaying
# every production run. Every design must therefore carry silkscreen on BOTH
# front (F.SilkS) and back (B.SilkS) layers. This check is a hard gate; there is
# deliberately no allowlist for single-sided boards — they get fixed, not exempted.
#
# Scans every design directory under DESIGN_ROOT (defaults to this script's own
# directory, i.e. Electrical/Design) for its primary board file — the
# "<name>/<name>.kicad_pcb" whose folder name matches the file name — and counts
# real silkscreen items on each layer. Only actual items written as
# `(layer "F.SilkS")` / `(layer "B.SilkS")` are counted (this includes footprint
# reference/value text). The board-level layer-stackup definition — e.g.
# `(37 "F.SilkS" user)` — is deliberately NOT counted, so an unused-but-declared
# layer still reads as empty. Variant folders whose name differs from the board
# file (e.g. "*_jlc_order") and ".history" autosaves are skipped.
#
# Usage:  check_silkscreen.sh [--github] [DESIGN_ROOT]
#   --github  also emit GitHub Actions error annotations and a run-summary table
#             (auto-enabled when GITHUB_ACTIONS=true). Does not change stdout.
#
# Output: a deterministic, sorted report on stdout (no timestamps, stable order).
# Exit status:
#   0  every design has both silkscreen layers populated
#   1  at least one design has an empty silkscreen layer
#   2  usage / environment error (bad path, no boards found)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

github_mode=0
[ "${GITHUB_ACTIONS:-}" = "true" ] && github_mode=1
positional=()
for arg in "$@"; do
  case "$arg" in
    --github) github_mode=1 ;;
    *)        positional+=("$arg") ;;
  esac
done
DESIGN_ROOT="${positional[0]:-$SCRIPT_DIR}"

if [ ! -d "$DESIGN_ROOT" ]; then
  echo "error: design root not found: $DESIGN_ROOT" >&2
  exit 2
fi

# Collect primary board files "<name>/<name>.kicad_pcb", excluding .history
# autosaves and name-mismatched variant folders. Sorted for determinism.
mapfile -t BOARDS < <(
  find "$DESIGN_ROOT" -type f -name '*.kicad_pcb' -not -path '*/.history/*' \
  | while IFS= read -r pcb; do
      dir="$(basename "$(dirname "$pcb")")"
      base="$(basename "$pcb" .kicad_pcb)"
      [ "$dir" = "$base" ] && printf '%s\n' "$pcb"
    done \
  | LC_ALL=C sort
)

if [ "${#BOARDS[@]}" -eq 0 ]; then
  echo "error: no design boards found under $DESIGN_ROOT" >&2
  exit 2
fi

# Count VISIBLE silk items on one layer ($1=layer name, $2=board file).
#
# A hidden item plots nothing, so a layer whose silk is entirely hidden still
# produces an empty gerber and must fail. KiCad writes text attributes in a
# fixed order, so a hidden item is exactly a `(layer "<name>")` line immediately
# followed by `(hide yes)`; those are excluded. Graphic lines/polys have no hide
# attribute and are always counted as visible.
count_layer() {
  awk -v layer="$1" '
    function trim(s){ gsub(/^[ \t\r]+|[ \t\r]+$/, "", s); return s }  # \r: some boards use CRLF
    {
      line = trim($0)
      if (pend) { if (line != "(hide yes)") c++; pend = 0 }
      if (line == "(layer \"" layer "\")") pend = 1
    }
    END { if (pend) c++; print c + 0 }
  ' "$2"
}

# --- gather results once -----------------------------------------------------
names=(); paths=(); fronts=(); backs=(); statuses=(); fail=0
for pcb in "${BOARDS[@]}"; do
  name="$(basename "$pcb" .kicad_pcb)"
  front="$(count_layer 'F.SilkS' "$pcb")"
  back="$(count_layer 'B.SilkS' "$pcb")"

  if [ "$front" -eq 0 ] && [ "$back" -eq 0 ]; then
    status="FAIL: front+back empty"; fail=1
  elif [ "$front" -eq 0 ]; then
    status="FAIL: front empty"; fail=1
  elif [ "$back" -eq 0 ]; then
    status="FAIL: back empty"; fail=1
  else
    status="ok"
  fi

  names+=("$name"); paths+=("$pcb"); fronts+=("$front"); backs+=("$back"); statuses+=("$status")
done

# --- deterministic stdout report ---------------------------------------------
printf '%-32s %6s %6s   %s\n' "DESIGN" "FRONT" "BACK" "STATUS"
printf '%-32s %6s %6s   %s\n' \
  "--------------------------------" "------" "------" "------------------------"
for i in "${!names[@]}"; do
  printf '%-32s %6d %6d   %s\n' \
    "${names[$i]}" "${fronts[$i]}" "${backs[$i]}" "${statuses[$i]}"
done
echo
if [ "$fail" -ne 0 ]; then
  echo "RESULT: FAIL — one or more designs have an empty silkscreen layer."
else
  echo "RESULT: PASS — all designs have front and back silkscreen."
fi

# --- optional GitHub Actions surfacing ---------------------------------------
if [ "$github_mode" -eq 1 ]; then
  for i in "${!names[@]}"; do
    # Annotations link to files only when the path is repo-relative; strip the
    # working-directory prefix (the repo root under Actions).
    rel="${paths[$i]#"$PWD"/}"
    case "${statuses[$i]}" in
      FAIL*) echo "::error file=${rel},title=Empty silkscreen::${names[$i]} — ${statuses[$i]}. Every design must have front and back silkscreen (manufacturer flags empty layers and delays production)." ;;
    esac
  done
  if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then
    {
      echo "## Silkscreen gate"
      echo
      if [ "$fail" -ne 0 ]; then
        echo "❌ **FAIL** — one or more designs have an empty silkscreen layer."
      else
        echo "✅ **PASS** — all designs have front and back silkscreen."
      fi
      echo
      echo '| Design | Front | Back | Status |'
      echo '| --- | ---: | ---: | --- |'
      for i in "${!names[@]}"; do
        echo "| ${names[$i]} | ${fronts[$i]} | ${backs[$i]} | ${statuses[$i]} |"
      done
    } >> "$GITHUB_STEP_SUMMARY"
  fi
fi

exit "$fail"
