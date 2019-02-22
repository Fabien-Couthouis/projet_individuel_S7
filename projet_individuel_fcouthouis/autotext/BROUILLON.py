import spacy
from spacy.pipeline import TextCategorizer
import requests
import PyPDF2
from PyPDF2 import PdfFileReader


url = 'https://arxiv.org/pdf/1706.05507.pdf'
path = "temp.pdf"
nlp = spacy.load('en')
# response = requests.get(url)
# my_raw_data = response.content

# with open("temp.pdf", 'wb') as my_data:
#     my_data.write(my_raw_data)

# open_pdf_file = open("temp.pdf", 'rb')
# read_pdf_file = PyPDF2.PdfFileReader(open_pdf_file)


# if read_pdf.isEncrypted:
#     read_pdf.decrypt("")
#     print(read_pdf.getPage(0).extractText())

# else:
#     print(read_pdf.getPage(0).extractText())


def get_content(url):
    response = requests.get(url)
    my_raw_data = response.content

    with open(path, 'wb') as my_data:
        my_data.write(my_raw_data)


def read():
    open_pdf_file = open(path, 'rb')
    content = PdfFileReader(open_pdf_file)
    return content


def get_info(pdf):
    info = pdf.getDocumentInfo()

    print(info)
    print('author : ' + info['/Author'])
    print('title : ' + info['/Title'])
    print('CreationDate : ' + info['/CreationDate'])


def text_extractor(pdf):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)

        # get the first page
        page = pdf.getPage(1)
        print(page)
        print('Page type: {}'.format(str(type(page))))

        text = page.extractText()
        print(text)


def content_from_text():
    pdf = read()
    firstPage = pdf.getPage(0)
    text = firstPage.extractText()
    # print(text)

    doc = nlp(text)

    dates = []
    pers = []
    titles = []
    for ent in doc.ents:
        if (ent.label_ == 'DATE'):
            dates.append([ent.text, ent.start_char, ent.end_char, ent.label_])

        if (ent.label_ == ('ORG' or 'PERSON')):
            pers.append([ent.text, ent.start_char, ent.end_char, ent.label_])

        if (ent.label_ == ('WORK_OF_ART')):
            titles.append([ent.text, ent.start_char, ent.end_char, ent.label_])

    print("DATE" + "\n ---------------------------------------------------")
    for d in dates:
        print("-----")
        print(d[0] + "__" + d[3])
        print("-----")

    print("ORG/PERS" + "\n ---------------------------------------------------")
    for p in pers:
        print("\n-----")
        print(p[0] + "__" + p[3])

    print("ORG/WORK_OF_ART" + "\n ---------------------------------------------------")
    for t in titles:
        print("-----")
        print(t[0] + "__" + t[3])
        print("-----")


textcat = TextCategorizer(nlp.vocab)
doc = nlp(u"This is a sentence.")
processed = textcat(doc)
