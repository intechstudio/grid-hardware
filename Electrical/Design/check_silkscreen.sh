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
# A genuinely one-sided design documents that with a `${LAYER} layer is
# intentionally empty...` marker text placed outside the board outline (see
# FP-BU16). Since that marker's whole claim is "nothing else is here," it must
# be the ONLY item on its layer — a layer carrying the marker plus real
# silkscreen also fails, even though its item count is nonzero.
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

# Does a "${LAYER} layer is intentionally empty..." marker text target this
# layer ($1=layer name, $2=board file)? The marker is our own convention for
# documenting a genuinely one-sided design (see FP-BU16); its whole point is
# that the layer has NO other content, so if real silkscreen coexists with it
# the marker's claim is false — and worse, it risks being plotted alongside
# real artwork. The marker's `(layer ...)` line always follows within a few
# lines of the text line itself, so a short lookahead window is enough.
marker_layer() {
  awk -v layer="$1" '
    function trim(s){ gsub(/^[ \t\r]+|[ \t\r]+$/, "", s); return s }
    {
      line = trim($0)
      if (line ~ /^\(gr_text "\$\{LAYER\} layer is intentionally empty/) { remaining = 8 }
      else if (remaining > 0) {
        remaining--
        if (line == "(layer \"" layer "\")") { found = 1; remaining = 0 }
      }
    }
    END { print found + 0 }
  ' "$2"
}

# --- gather results once -----------------------------------------------------
names=(); paths=(); fronts=(); backs=(); statuses=(); fail=0
for pcb in "${BOARDS[@]}"; do
  name="$(basename "$pcb" .kicad_pcb)"
  front="$(count_layer 'F.SilkS' "$pcb")"
  back="$(count_layer 'B.SilkS' "$pcb")"
  front_marker="$(marker_layer 'F.SilkS' "$pcb")"
  back_marker="$(marker_layer 'B.SilkS' "$pcb")"

  problems=()
  [ "$front" -eq 0 ] && problems+=("front empty")
  [ "$back" -eq 0 ] && problems+=("back empty")
  [ "$front" -gt 1 ] && [ "$front_marker" -eq 1 ] && problems+=("front has real silkscreen alongside empty-marker")
  [ "$back" -gt 1 ] && [ "$back_marker" -eq 1 ] && problems+=("back has real silkscreen alongside empty-marker")

  if [ "${#problems[@]}" -eq 0 ]; then
    notes=()
    [ "$front" -eq 1 ] && [ "$front_marker" -eq 1 ] && notes+=("front: empty marker detected")
    [ "$back" -eq 1 ] && [ "$back_marker" -eq 1 ] && notes+=("back: empty marker detected")
    if [ "${#notes[@]}" -eq 0 ]; then
      status="ok"
    else
      status="ok ($(IFS='; '; echo "${notes[*]}"))"
    fi
  else
    fail=1
    status="FAIL: $(IFS='; '; echo "${problems[*]}")"
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
      if [ "$fail" -ne 0 ]; then
        echo "❌ Silkscreen: ${#names[@]} design(s) checked — one or more have an empty silkscreen layer"
        echo
        echo '| Design | Front | Back | Status |'
        echo '| --- | ---: | ---: | --- |'
        for i in "${!names[@]}"; do
          echo "| ${names[$i]} | ${fronts[$i]} | ${backs[$i]} | ${statuses[$i]} |"
        done
      else
        echo "✅ Silkscreen: ${#names[@]} design(s) checked — all have front and back silkscreen"
      fi
    } >> "$GITHUB_STEP_SUMMARY"
  fi
fi

exit "$fail"
