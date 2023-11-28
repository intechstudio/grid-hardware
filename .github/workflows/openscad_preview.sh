cd ./temp || exit

# Iterate through all STL files in the temp folder
for stl_file in *.stl; do
    # Temporary OpenSCAD script file
    tmp_script="__tmp__$stl_file"

    # Extract the file name without extension
    filename_no_ext="${stl_file%.*}"

    # Generate OpenSCAD script
    echo "import(\"$stl_file\");" > "$tmp_script"

    cat "$tmp_script"

    # Generate PNG preview using OpenSCAD
    xvfb-run -a openscad -o "$filename_no_ext.png" --colorscheme=Tomorrow --imgsize=3200,2400 "$tmp_script"

    # Remove the temporary OpenSCAD script
    rm "$tmp_script"
done

echo "PNG previews generated successfully in ./temp"