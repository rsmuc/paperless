import subprocess
import os
from shutil import copyfile
import traceback



verapdf_path = "" # "~/verapdf2/"
ignore = "Alte Dokumente"
# Ignore files and folders containing the ignore pattern
disable_ignore = False


count_ok = 0
count_nok = 0
broken_documents = []

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
    
    print ("\n Verifiy:" + file)

    p=subprocess.Popen("%sverapdf '%s'" % (verapdf_path , file), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read()
        
    if "compliant=\"1\"" in str(result):
        print("OK")
        count_ok = count_ok + 1
    else:
        print("DOCUMENT BROKEN")
        count_nok = count_nok + 1
        broken_documents.append(file)
    if "verapdf: not found" in str(result):
        print("ERROR: VERA PDF NOT FOUND")
        break
        
        
print ("################################\n"
"################################\n"
"################################\n"
"\n "
"\n"
"\n"
"COMPLIANT DOCUMENTS: %s\n”" 
"NONCOMPLIANT DOCUMENTS: %s\n"
"\n"
"\n"
"\n"
"NON COMPLIANT FILES:\n"
"%s" % (str(count_ok), str(count_nok), "\n".join(broken_documents)))


        
        
    
    
