# import spacy
# from spacy_cld import LanguageDetector
import io
import pybtex.database.input.bibtex
import six
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey


class Reference(models.Model):

    url = models.URLField(max_length=400)
    _bibtex_reference = models.TextField(null=True,)
    apa_reference = models.TextField(blank=True, null=True,)
    _content = models.TextField(blank=True, null=True, editable=False)
    webography = GenericForeignKey("autotext.Webography")
    # webography = models.ForeignKey("Webography", on_delete=models.CASCADE, related_name="webography_references")

    # class Meta:
    #     abstract = True

    # Needs to be stored as a class variable
    # language_detector = LanguageDetector()

    def __str__(self):
        return self.url

    def _get_content(self):
        """Get the raw content of the article (html or text). """
        raise NotImplementedError('subclasses must override get_content()!')

    @property
    def bibtex_reference(self):
        """
        Get the bibtex reference. Returns a string.
        """
        raise NotImplementedError(
            'subclasses must override get_bibtext_reference()!')

    @bibtex_reference.setter
    def bibtex_reference(self, value):
        self._bibtex_reference = value

    def get_formatted_reference(self, formatStyle='apa'):
        """
        Get the reference formatted into one of the possible formats.
        FormatStyle can be 'alpha', 'plain', 'unsrt', 'unsrtalpha' or 'apa'. Default = 'apa'.
        """
        bibref = self.bibtex_reference()

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

        # We remove "\n" at the end of the output value
        formatted_ref = output.getvalue().replace("\n", "")

        return formatted_ref

    # def get_language(self, text=""):
    #     nlp = spacy.load('en')
    #     nlp.add_pipe(Reference.language_detector)
    #     doc = nlp(text)

    #     return doc._.languages

    def log_error(self, e):
        print(e)
