# import spacy
# from spacy_cld import LanguageDetector
from abc import ABC, abstractmethod, ABCMeta
import pybtex.database.input.bibtex
import six
import io


class Article(ABC):
    # Need to be stored as a class variable
    # language_detector = LanguageDetector()

    def __init__(self, url=""):
        self.url = url
        self.content = None

    def __str__(self):
        return self.url

    @abstractmethod
    def get_content(self):
        """Get the raw content of the article (html or text). """
        raise NotImplementedError('subclasses must override get_content()!')

    @abstractmethod
    def get_bibtex_reference(self):
        """
        Get the bibtex reference. Returns a string.
        """
        raise NotImplementedError(
            'subclasses must override get_bibtext_reference()!')

    def get_formatted_reference(self, formatStyle='apa'):
        """
        Get the reference formatted into one of the possible formats.
        FormatStyle can be 'alpha', 'plain', 'unsrt', 'unsrtalpha' or 'apa'. Default = 'apa'.
        """
        bibref = self.get_bibtex_reference()

        pybtex_style = pybtex.plugin.find_plugin(
            'pybtex.style.formatting', formatStyle)()
        pybtex_html_backend = pybtex.plugin.find_plugin(
            'pybtex.backends', 'text')()
        pybtex_parser = pybtex.database.input.bibtex.Parser()

        data = pybtex_parser.parse_stream(six.StringIO(bibref))
        data_formatted = pybtex_style.format_entries(
            six.itervalues(data.entries))
        output = io.StringIO()
        pybtex_html_backend.write_to_stream(data_formatted, output)

        return output.getvalue()

    # def get_source(self, standardType='apa'):
    #     if standardType == 'apa':
    #         # NomAuteur, Initiales. (année). TitreDocument. Consulté sur http: // WebAdress
    #         apa = self.author_name + \
    #             " (" + self.publication_date + ") " + \
    #             self.title + ". Consulté sur : " + self.url

    #         return apa
    #     else:
    #         return ""

    # def get_language(self, text=""):
    #     nlp = spacy.load('en')
    #     nlp.add_pipe(Article.language_detector)
    #     doc = nlp(text)

    #     return doc._.languages

    def log_error(self, e):
        print(e)
