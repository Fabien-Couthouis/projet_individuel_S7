import time
import gscholar
import spacy
# from spacy.pipeline import TextCategorizer
import requests
import PyPDF2
from PyPDF2 import PdfFileReader
from pdftitle import get_title
import tempfile
# import .models
from .models.source import Source
from .models.sourcePDF import SourcePDF


url = 'https://arxiv.org/pdf/1706.05507.pdf'
path = "temp/temp.pdf"
nlp = spacy.load('en')


def get_content(url):
    response = requests.get(url)
    my_raw_data = response.content
    tempPDF = tempfile.NamedTemporaryFile()
    tempPDF.write(my_raw_data)

    return tempPDF

    # with open(path, 'wb') as my_data:
    #     my_data.write(my_raw_data)


def get_bibtex(title):
    queries = gscholar.query(title)
    for query in queries:
        print(query)
    return queries


def get_source(file):
    title = get_title(file.name)
    source = get_bibtex(title)
    file.close()
    return source


source = SourcePDF("https://arxiv.org/pdf/1706.05507.pdf")
print(source.get_metadata())
