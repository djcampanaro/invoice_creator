from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from PIL import Image

# from PyPDF2 import PdfReader

# reader = PdfReader('invoice_template.pdf')
# number_of_pages = len(reader.pages)
# page = reader.pages[0]
# text = page.extract_text()
# print(text)



# document = []
# document.append(Image('logo.png', 2.2*inch, 2.2*inch))
# document.append(Image('invoice_template.png', 8.33*inch, 10.83*inch))
# print(document)

# def addTitle(doc):
#     doc.append(Spacer(1, 20))
#     doc.append(Paragraph('Test File', ParagraphStyle(name='Name',
#                                                      fontFamily='Calibri',
#                                                      fontSize=24,
#                                                      alignment=TA_CENTER)))
#     doc.append(Spacer(1, 50))
#     return doc


# def addParagraphs(doc):
#     with open('text.txt') as txt:
#         for line in txt.read().split('\n'):
#             doc.append(Paragraph(line))
#             doc.append(Spacer(1, 12))
#     return doc

# document = addTitle(document)
# document = addParagraphs(document)

# SimpleDocTemplate('test_file.pdf', pagesize=letter, rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0).build(document)


# 611 x 791
def hello(c):
    box = [(50, 741, 561, 741),(50, 50, 50, 741),(561, 741, 561, 50),(561, 50, 50, 50),(305, 791, 305, 0),(286, 741, 286, 700),(324, 741, 324, 700)]
    # image = Image.open('invoice_template.png')
    # c.drawImage('invoice_template.png', 500, 500, mask=None)
    c.lines(box)
    c.setFont('Helvetica', 24)
    c.drawString(275, 710, 'Invoice')
    c.setFont('Helvetica', 14)
    c.drawString(50, 715, 'Dominic Campanaro')

c = canvas.Canvas("hello.pdf", pagesize=letter)
hello(c)
c.showPage()
c.save()
