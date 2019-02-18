import spacy
from spacy_cld import LanguageDetector
from .contentExtractionSite import ContentExtractionSite
from datetime import datetime


class Source():

    # Need to be stored as a class variable
    language_detector = LanguageDetector()

    def __init__(self, url=""):
        self.url = url
        self.CE = ContentExtractionSite()
        self.language = ""
        self.title = ""
        self.author_name = ""
        self.publication_date = ""
        self.last_consultation_date = ""

    def __str__(self):
        return self.url

    def get_source(self, standardType='apa'):
        if standardType == 'apa':
            # NomAuteur, Initiales. (année). TitreDocument. Consulté sur http: // WebAdress
            apa = self.author_name + \
                " (" + self.publication_date + ") " + \
                self.title + ". Consulté sur : " + self.url

            return apa
        else:
            return ""

    def get_language(self, text=""):
        nlp = spacy.load('en')
        nlp.add_pipe(Source.language_detector)
        doc = nlp(text)

        return doc._.languages

    def get_data(self):
        self.language = self.get_language()
        self.title = self.CE.get_title()
        self.author_name = self.CE.get_author_name()
        self.publication_date = self.CE.get_author_name()
        self.format_publication_date()
        self.last_consultation_date = datetime.now().isoformat()

    def format_publication_date(self):
        isoStringPD = self.publication_date
        dt = datetime.strptime(isoStringPD, "%Y-%m-%dT%H:%M:%S%z")
        apaPublicDate = datetime.strftime(dt, "%Y, %d %B")
        return apaPublicDate
