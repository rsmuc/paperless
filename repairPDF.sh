find . -type f -name '*.pdf' -not -path '*Alte*' -print0 | while IFS= read -r -d '' file;
do
echo "$file"

if verapdf "$file" > /dev/null; then
    echo PDF is valid
else
    echo PDF is not valid
    echo Fix with OCRmyPDF
    docker run --rm -v $(pwd):/data -i jbarlow83/ocrmypdf --tesseract-timeout=0 --skip-text "/data/$file" "/data/$file"
fi
done
