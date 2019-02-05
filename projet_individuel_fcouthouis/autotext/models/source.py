from datetime import date
import spacy
from spacy_cld import LanguageDetector
# import contentExtraction


class Source():

    # Need to be stored as a class variable
    language_detector = LanguageDetector()

    # def __init__(self):
    # url = ""
    # language = ""
    # title = ""
    # author_firstname = ""
    # author_lastname = ""
    # publication_date = date.today()
    # last_consultation_date = date.today()

    def get_language(self, text):
        nlp = spacy.load('en')
        nlp.add_pipe(Source.language_detector)
        doc = nlp(text)

        return doc._.languages

    def get_data(self):
        return self

    def format(self):
        formattedSource = ""
        return formattedSource

    # def get_text(self):

    #     return
