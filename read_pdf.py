# This is a simplified version of pdfminer's pdf2txt.py,
# providing a read_pdf function to turn a pdf into txt with default opts.

import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

# main
def read_pdf(pdf):
    password = ''
    pagenos = set()
    maxpages = 0
    imagewriter = None
    rotation = 0
    codec = 'utf-8'
    caching = True
    laparams = LAParams()
    rsrcmgr = PDFResourceManager(caching=caching)

    import StringIO
    outfp = StringIO.StringIO()

    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)

    fp = StringIO.StringIO(pdf)

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos,
                                maxpages=maxpages, password=password,
                                caching=caching, check_extractable=True):
        page.rotate = (page.rotate+rotation) % 360
        interpreter.process_page(page)
    fp.close()
    device.close()
    v = outfp.getvalue()
    outfp.close()
    return v

if __name__ == "__main__":
    pdf = open("sample.pdf", "r").read()
    print read_pdf(pdf)
