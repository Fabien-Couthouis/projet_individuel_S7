import spacy
from spacy_cld import LanguageDetector
from abc import ABC, abstractmethod


class Article(ABC):

    # Need to be stored as a class variable
    language_detector = LanguageDetector()

    def __init__(self, url=""):
        self.url = url
        self.content = None
        # self.CE = ContentExtractionSite()
        # self.language = ""
        # self.title = ""
        # self.author_name = ""
        # self.publication_date = ""
        # self.last_consultation_date = ""

    def __str__(self):
        return self.url

    @abstractmethod
    def get_content(self):
        raise NotImplementedError('subclasses must override get_content()!')

    # def get_source(self, standardType='apa'):
    #     if standardType == 'apa':
    #         # NomAuteur, Initiales. (année). TitreDocument. Consulté sur http: // WebAdress
    #         apa = self.author_name + \
    #             " (" + self.publication_date + ") " + \
    #             self.title + ". Consulté sur : " + self.url

    #         return apa
    #     else:
    #         return ""

    def get_language(self, text=""):
        nlp = spacy.load('en')
        nlp.add_pipe(Article.language_detector)
        doc = nlp(text)

        return doc._.languages

    def log_error(self, e):
        print(e)
