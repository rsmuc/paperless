#requires PyMuPDF
#required PyPDF2

from PyPDF2 import PdfFileWriter, PdfFileReader
import fitz
import os
from shutil import copyfile

all_pdfs = []
ignore = "Alte Dokumente"
threshold = 7000


# find all PDFs in the subdirectories
for dirpath, dirs, files in os.walk("."):
    for filename in files:
        fname = os.path.join(dirpath, filename)
        if fname.endswith('.pdf') or fname.endswith('.PDF'):
            if ignore not in fname or disable_ignore:
                all_pdfs.append(fname)

# traverse all pdf files

for file in all_pdfs:

    print(file)

    doc = fitz.open(file)

    pagecount = doc.pageCount
    pages_to_keep = list(range(1, pagecount+1))
    pages_to_remove = []

    for i, page in enumerate(doc, 1):
        pix = page.getPixmap()
        size = len(pix.getImageData(output="png"))
        print("Size page " + str(i) + ": "+ str(size))
        if size < threshold:
            print("below threshold")
            pages_to_keep.remove(i)
            pages_to_remove.append(i)


    if len(pages_to_keep) < pagecount:

        #copy of the original file
        print("create a copy of the " + file)
        copyfile(file, (file + "_ORIGINAL_"))
        print("Empty pages: " + str(pages_to_remove))

        input = PdfFileReader(file, 'rb')
        output = PdfFileWriter()

        # the empty pages to crosscheck
        for i in pages_to_remove:
            p = input.getPage(i-1)
            output.addPage(p)

        print("Generate file with empty pages")
        with open(file+"_EMPTYPAGES_", 'wb') as f:
            output.write(f)

        output = PdfFileWriter()

        # the new file without empty pages
        print("Generate clean file")
        for i in pages_to_keep:
            p = input.getPage(i-1)
            output.addPage(p)

        with open(file, 'wb') as f:
            output.write(f)
