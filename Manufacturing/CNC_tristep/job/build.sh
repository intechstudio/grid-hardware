NOW=$(date +20"%y%m%d")

cat 0begin.gcode 1slow.gcode 2adaptive.gcode 3contour.gcode > canvas_cnc_job_$NOW.gcode
