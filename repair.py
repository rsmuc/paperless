import subprocess
import os

verapdf_path = "" # "~/verapdf2/"
ignore = "Alte Dokumente"
# Ignore files and folders containing the ignore pattern
disable_ignore = False

# traverse the folder and search for pdf files

all_pdfs = []


# find all PDFs in the subdirectories
for dirpath, dirs, files in os.walk("."): 
  for filename in files:
    fname = os.path.join(dirpath,filename)
    if fname.endswith('.pdf'):      
        if ignore not in fname or disable_ignore:
            all_pdfs.append(fname)
      

#traverese all pdf files

for file in all_pdfs:
    
    print ("\n Test:" + file)

    p=subprocess.Popen("%sverapdf '%s'" % (verapdf_path , file), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read()
        
    if "compliant=\"1\"" in str(result):
        print("OK")
        
    else:
        print("DOCUMENT BROKEN")
        p = subprocess.Popen("docker run --rm -v $(pwd):/data -i jbarlow83/ocrmypdf --tesseract-timeout=0 --skip-text '/data/%s' '/data/%s'" % (file, file), shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        result = p.stdout.read()
        print(result)

    if "verapdf: not found" in str(result):
        print("ERROR: VERA PDF NOT FOUND")
        break