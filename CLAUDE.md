# Project instructions

## KiCad library — easyeda2kicad downloads

`Electrical/Library/KiCad/download.sh` runs `easyeda2kicad` to pull parts from
LCSC/EasyEDA into `suku_basics`. It does **not** pass `--project-relative`, so
the 3D model path written into the generated `.kicad_mod` footprint is a bare
relative path (e.g. `suku_basics.3dshapes/FOO.wrl`), which only resolves if
the CWD happens to be `Library/KiCad` — it breaks when the footprint is used
from an actual `PCBA-*` project.

Every other footprint in `suku_basics.pretty` uses a project-relative path
anchored via `${KIPRJMOD}`:

```
(model "${KIPRJMOD}/../../Library/KiCad/suku_basics.3dshapes/FOO.wrl"
```

After running `download.sh`, manually fix the `model` line in the new
`.kicad_mod` file(s) to match this convention before committing.

## Creating a hardware variant (cloning a PCBA-* design)

Workflow validated cloning `PCBA-BU16` (RP2350A) into `PCBA-PO16`. Use the
design closest to the new board electrically as BASE — if it already shares
the CI baseline's `MCU`/`GRID`/`USB_POWER` sheets byte-for-byte (see below),
most of this is mechanical.

1. **Clone the directory**: `cp -r Electrical/Design/PCBA-BASE
   Electrical/Design/PCBA-NEW`. Strip BASE's own scratch/backup state that
   shouldn't ship in the clone: `PCBA-BASE-backups/`, `*.kicad_pcb-bak`,
   `*.kicad_pro-bak`, `kibot_error.log`, `kibot.mak`, `mfg-bot/`.

2. **Rename the four project-identity files**: `PCBA-BASE.kicad_pcb`,
   `.kicad_prl`, `.kicad_pro`, `.kicad_sch` → `PCBA-NEW.*`. Sub-sheet files
   (`MCU.kicad_sch`, `GRID.kicad_sch`, `UI_*.kicad_sch`, …) keep their names
   — `Sheetfile` properties reference those directly, not project-qualified.

3. **Rewrite every internal `"PCBA-BASE"` string to `"PCBA-NEW"`** across
   the new directory (`grep -rl "PCBA-BASE" . | xargs sed -i
   's/PCBA-BASE/PCBA-NEW/g'`). KiCad embeds the owning-project name inside
   each shared sheet's `(instances (project "NAME" ...))` blocks — leaving
   these stale makes KiCad misattribute sheet-instance data on open. This
   same substitution also covers the `Makefile`'s `SCH=`/`PCB=` vars, so
   there's no separate step for that.

4. **Sanity-scan for lingering references**: `grep -rni "BASE" .` in the
   new directory. Anything left is almost always harmless KiCad-cached
   editor state (e.g. a stale last-used VRML/STEP export path in
   `.kicad_pro` — cosmetic, outside `board.design_settings`/`erc`, not
   worth fixing) rather than something load-bearing — but check for
   yourself, don't just assume.

5. **Port over any board-specific sheets BASE doesn't have** (e.g. a
   `UI_POT` sheet for a pot-driven board) from wherever the previous
   revision of NEW lived, and wire them into `PCBA-NEW.kicad_sch`'s sheet
   hierarchy in KiCad. Drop whatever BASE-specific sheets NEW doesn't
   actually need — `check_annotation.py`'s orphan check (step 8 below)
   will fail on any `*.kicad_sch` left in the folder but unreferenced from
   the root sheet, so remove them once you're done rewiring.

6. **Hand-edit `HWCFG.kicad_sch`** for NEW's actual pinout/peripheral
   config — this sheet is per-board, never shared/baselined, so the cloned
   copy is only ever a placeholder.

7. **Re-annotate in KiCad** (Tools > Annotate Schematic) any time the
   sheet hierarchy changes — adding/removing/rewiring sheets shifts page
   numbers and reference-designator blocks.

8. **Register NEW in CI**, `.github/workflows/electrical_boards.yml`:
   - Add `PCBA-NEW` to the `preflight-check` job's matrix (schematic
     drift, DRC/ERC settings drift, annotation, and zone-outline-grid
     alignment — all four gates, described below).
   - Add `PCBA-NEW` to `generate-artifacts`'s `board:` matrix (fabrication
     export) if it isn't already there.

9. **Run the preflight checks locally** before pushing (`BASELINE_DESIGN`
   is currently `PCBA-EF44`):
   ```
   ./Electrical/Design/check_schematic_drift.py \
     --designs Electrical/Design/PCBA-EF44 Electrical/Design/PCBA-NEW \
     --sheets USB_POWER GRID MCU
   ./Electrical/Design/check_design_rules_drift.py \
     --designs Electrical/Design/PCBA-EF44 Electrical/Design/PCBA-NEW
   ./Electrical/Design/check_annotation.py --project Electrical/Design/PCBA-NEW
   ./Electrical/Design/check_zone_grid.py --project Electrical/Design/PCBA-NEW
   ./Electrical/Design/check_silkscreen.sh
   ```
   The first two are comparative (must match the baseline exactly, modulo
   documented per-project noise); annotation and zone-grid are absolute
   (validate NEW's own internal consistency, not agreement with another
   design).

10. **Run the real DRC/ERC**, not just the settings-drift check, once
    routing is done — `kicad-cli pcb drc`/`sch erc
    --severity-error --severity-warning --format json`. Compare violation
    types/counts against BASE as a sanity baseline rather than expecting
    zero: this repo's boards routinely carry warning-level
    `silk_over_copper`/`courtyards_overlap`/etc. Treat only `error`-severity
    results and large outliers vs. BASE as real problems.

11. **Copper zones**: if zones were cloned/copied from another board,
    their `clearance`/`min_thickness` and outline-vertex grid alignment
    must match this repo's convention — `check_zone_grid.py` enforces the
    outline vertices sit on a 1mm raster (checks the zone's own
    `(polygon (pts ...))`, not the derived `(filled_polygon ...)`). After
    hand-editing any zone outline, **re-fill and re-save** before trusting
    the board: `kicad-cli pcb drc --refill-zones --save-board <file>`.

12. **Clean up before committing**: KiCad `~*.lck` lock files (project
    still open somewhere), and `PCBA-NEW-backups/` (KiCad's autosave dir,
    same as the one stripped from BASE in step 1).

13. **Decide the fate of any pre-existing legacy version of NEW** (e.g. a
    `PCBA-NEW-BAK` backed up before starting the clone) once anything
    reusable has been salvaged from it — delete, or rename to something
    clearly archival (`PCBA-NEW-LEGACY`).
