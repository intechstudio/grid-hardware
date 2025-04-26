for file in *.pdf; do
  basename="${file%.pdf}"
  pdf2svg "$file" "${basename}.svg"
done
