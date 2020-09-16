import os
import datetime
import re
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import dateutil.parser as dparser

past_delta = 60
future_delta = 1

def get_all_pdfs():
    all_pdfs = []
    ignore = "Alte Dokumente"
    # Ignore files and folders containing the ignore pattern
    disable_ignore = False

    # find all PDFs in the subdirectories
    for dirpath, dirs, files in os.walk("."):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            if fname.endswith('.pdf') or fname.endswith('.PDF'):
                if ignore not in fname or disable_ignore:
                    all_pdfs.append(fname)

    return all_pdfs

def get_text_from_pdf(file):
    output_string = StringIO()
    with open(file, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

        text = output_string.getvalue()

    return text

def check_with_regex(text):
    dates = []

    for line in text.splitlines():
        for expression in line.split(" "):
            result = re.findall(
                "^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])$|^([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$",
                expression)
            if result:
                date = ".".join(result[0])
                dates.append(dparser.parse(date, fuzzy=False, dayfirst=True))
    return dates


def check_with_dparser(text, fuzzy=False):
    dates = []

    for line in text.splitlines():

        try:
            dates.append(dparser.parse(line, fuzzy=fuzzy, dayfirst=True))

        except:
            continue

    return dates


# traverse the folder and search for pdf files
all_pdfs = get_all_pdfs()

#traverese all pdf files and get the text
for file in all_pdfs:

    print("------------------------------------------------------")

    # check if there is already a date in the filename
    if file.count("-") > 1 :
        print(file + " already has a date")
        continue
    
    print("Guessing the date for file in content" + file)
    
    text = get_text_from_pdf(file)

    dates = []
    dates = check_with_dparser(text)

    if len(dates) == 0:
        print("WARNING: No date found with dparser, try regex")
        dates = check_with_regex(text)

    if len(dates) == 0:
        print("WARNING: Still no date found, try dparser with fuzzy")
        dates = check_with_regex(text, True)

    if len(dates) == 0:
        print("ERROR: No date found at all")
        continue

    # we will use the first found date ... that should be correct usually
    real_date = dates[0].strftime("%Y-%m-%d")
    print("FOUND DATE: " + real_date)

    # Plausicheck

    diff = datetime.datetime.now() - dates[0]
    print("Difference to today: " + str(diff))

    if diff > datetime.timedelta(days=past_delta) or diff < datetime.timedelta(days=future_delta):
        print("ERROR: Diff from Document date too high - Check manually")
        continue

    # rename the file
    new_name = real_date + " " + file.replace('./', '')
    print("Rename to '" + new_name + "'")
    os.rename(file, new_name)
    print("------------------------------------------------------")

print("Done")