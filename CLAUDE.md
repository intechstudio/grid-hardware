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
