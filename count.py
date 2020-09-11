#from PyPDF2 import PdfFileReader
import os

count = 0
ignore = "Alte Dokumente"
not_readable = []
# Ignore files and folders containing the ignore pattern
disable_ignore = False

all_pdfs = []

# find all PDFs in the subdirectories
for dirpath, dirs, files in os.walk("."):
    for filename in files:
        fname = os.path.join(dirpath, filename)
        if fname.endswith('.pdf') or fname.endswith('.PDF'):
            if ignore not in fname or disable_ignore:
                all_pdfs.append(fname)

# traverese all pdf files

for file in all_pdfs:

    try:
        cmd = "pdfinfo '%s' | grep 'Pages' | awk '{print $2}'" % file
        pages = (os.popen(cmd).read().strip())
        count = count + int(pages)

        print(file + ": " + str(pages) + " pages; in total: " + str(count))

    except ValueError:
        print("could not read " + file)
        not_readable.append(file)
        continue

print("NOT READABLE:")
for file in not_readable:
    print(file)

print ("ALL PAGES: " + str(count))
