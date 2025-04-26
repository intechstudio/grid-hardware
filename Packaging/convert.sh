for file in *.pdf; do
  basename="${file%.pdf}"
  pdf2svg "$file" "${basename}.svg"
  pdftoppm -png -singlefile "$file" "${basename}"
done
