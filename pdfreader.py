from PyPDF2 import PdfFileReader, PdfFileWriter
import camelot, os, sys, os.path
from os import path
import pandas as pd
import sheets_pdfreader
import subprocess, webbrowser

try:
    date_prefix = sys.argv[1]
except IndexError:
    date_prefix = input("\nWow\nThat was an early mistake! Did you also for get to download the files today too?\n\nWhat's the prefix du jour? ")

def csvize(file_path_in):
    # file_path = "/Users/Throsby/Documents/GitHub/PDF_Reader/Test PDFs/427workingsplinter.pdf"
    file_path = "/Users/Throsby/Documents/GitHub/PDF_Reader/Test PDFs/{}{}ing.pdf".format(date_prefix,file_path_in)
    ###Handle the various ways that I might forget to include the date ###
    try:
        f = open(file_path,'rb')
        pdf = PdfFileReader(f)
    except FileNotFoundError:
        try:
            corrected_date_prefix = input("File not found, what date did you forget? ")
            if(corrected_date_prefix=="None"):
                pass
            file_path = "/Users/Throsby/Documents/GitHub/PDF_Reader/Test PDFs/{}{}ing.pdf".format(date_prefix,file_path_in)
            f = open(file_path,'rb')
            pdf = PdfFileReader(f)
        except FileNotFoundError:
            corrected_date_prefix = input("\nGet it together, bud.\nLast shot!\n\nFile not found, what date did you mean? ")
            file_path = "/Users/Throsby/Documents/GitHub/PDF_Reader/Test PDFs/{}{}ing.pdf".format(date_prefix,file_path_in)
            f = open(file_path,'rb')
            pdf = PdfFileReader(f)


    ### Creates name of file without filetype as tail_wo_filetype. Creates procedure as the first four letters of tail_wo_filetype
    head, tail_with_filetype = os.path.split(file_path)
    tail_wo_filetype = os.path.splitext(tail_with_filetype)[0]
    procedure = tail_wo_filetype[:4]

    ### Saves the pages of the input pdf to the
    for page in range(pdf.numPages):
        output = PdfFileWriter()
        output.addPage(pdf.getPage(page))
        with open("temp%s.pdf"%(page),"wb") as outputStream:
            output.write(outputStream)

    pdf_tables = pd.DataFrame()
    f.close()
    pd.set_option('display.max_rows', None)

    ###Turn the temporary pdfs into TableList objects and delete the temp pdfs
    for page in range(pdf.numPages):
        working_on = "/Users/Throsby/Documents/GitHub/PDF_Reader/temp%s.pdf"%(page)
        sheet = camelot.read_pdf(working_on, flavor='lattice', line_scale=60)

        for table in range(0,sheet.n):
            pdf_tables = pdf_tables.append(sheet[table].df)
        os.remove(working_on)
    print(pdf_tables)

    pdf_tables.to_csv("%s.csv"%(tail_wo_filetype), index=False)
    print("%s.csv Done!"%(tail_wo_filetype))

# HERE for custom surprise formatting
# sheets_pdfreader.make_sheet_up(file_path)
for file in ["work","test","fitt"]:
    pathstring = "/Users/Throsby/Documents/GitHub/PDF_Reader/Test PDFs/{}{}ing.pdf".format(date_prefix,file)
    if(path.exists(pathstring)):
        csvize(file)
        fileydo = "/Users/Throsby/Documents/GitHub/PDF_Reader/Test PDFs/{}{}ing.pdf".format(date_prefix,file)
        runner = subprocess.Popen(['open','-a','Adobe Acrobat Reader DC',fileydo], shell=False)
        sheets_pdfreader.make_sheet_up(pathstring)
    else:
        print("{}{}ing.pdf doesn't exist!".format(date_prefix,file))
        continue
