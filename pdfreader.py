from PyPDF2 import PdfFileReader, PdfFileWriter
import camelot, os
import pandas as pd

test_path = "/Users/Throsby/Desktop/PDF Reader Project/Test PDFs/temp0.pdf"
fit_path = "/Users/Throsby/Desktop/PDF Reader Project/Test PDFs/working211.pdf"
shoot_path = "/Users/Throsby/Desktop/PDF Reader Project/Test PDFs/shooting.pdf"

pdf = PdfFileReader(open(test_path,'rb'))



### Saves the pages of the input pdf to the
for page in range(pdf.numPages):
    output = PdfFileWriter()
    output.addPage(pdf.getPage(page))
    with open("temp%s.pdf"%(page),"wb") as outputStream:
        output.write(outputStream)

pdf_tables = pd.DataFrame()
# pd.set_option('display.max_rows', None)
###Turn the temporary pdfs into TableList objects and delete the temp pdfs
for page in range(pdf.numPages):
    working_on = "/Users/Throsby/Desktop/PDF Reader Project/temp%s.pdf"%(page)
    sheet = camelot.read_pdf(working_on, flavor='lattice', line_scale=60)
    for table in range(0,sheet.n):
        pdf_tables = pdf_tables.append(sheet[table].df)
    os.remove(working_on)
print(pdf_tables)


pdf_tables.to_csv("output.csv")
