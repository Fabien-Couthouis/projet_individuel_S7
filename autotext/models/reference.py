# import spacy
# from spacy_cld import LanguageDetector
import io
import pybtex.database.input.bibtex
import six
from django.db import models
import re


class Reference(models.Model):
    url = models.URLField(max_length=400)
    _bibtex_reference = models.TextField(null=True,)
    _apa_reference = models.TextField(blank=True, null=True,)
    webography = models.ForeignKey(
        "Webography", on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        string = "Reference : " + str(self.pk) + " with url : " + str(self.url)
        return string

    @property
    def bibtex_reference(self):
        if self._bibtex_reference is None or self._bibtex_reference == "":
            self._bibtex_reference = self._get_bibtex_reference()
            self.save()
            print("ACCESS TO GETTER")

        return self._bibtex_reference

    @bibtex_reference.setter
    def bibtex_reference(self, value):
        self._bibtex_reference = value

    @property
    def apa_reference(self):
        if self._apa_reference is None or self._apa_reference == "":
            self._apa_reference = self._get_formatted_reference('apa')
            self.save()

        return self._apa_reference

    @apa_reference.setter
    def apa_reference(self, value):
        self._apa_reference = value

    def _retrieve_content(self):
        """Get the raw content of the article (html or binaries from pdf). """
        raise NotImplementedError(
            'subclasses must override _retrieve_content()!')

    def _get_bibtex_reference(self):
        """
        Get the bibtex reference. Returns a string.
        """
        raise NotImplementedError(
            'subclasses must override get_bibtext_reference()!')

    def _get_formatted_reference(self, formatStyle='apa'):
        """
        Get the reference formatted into one of the possible formats.
        FormatStyle can be 'alpha', 'plain', 'unsrt', 'unsrtalpha' or 'apa'. Default = 'apa'.
        """

        # Return "" if bibtex ref is not referenced, as we need bibtex ref to find apa reference
        if self.bibtex_reference == "undefined" or self.bibtex_reference is None:
            return "undefined"
        else:
            pybtex_style = pybtex.plugin.find_plugin(
                'pybtex.style.formatting', formatStyle)()
            pybtex_html_backend = pybtex.plugin.find_plugin(
                'pybtex.backends', 'text')()
            pybtex_parser = pybtex.database.input.bibtex.Parser()

            data = pybtex_parser.parse_stream(
                six.StringIO(self.bibtex_reference))
            data_formatted = pybtex_style.format_entries(
                six.itervalues(data.entries))
            output = io.StringIO()
            pybtex_html_backend.write_to_stream(data_formatted, output)

            # Remove "\n" at the end of the output value
            formatted_ref = output.getvalue().replace("\n", "")

            # Remove useless array at the begining
            formatted_ref = re.sub(r'\[(.*?)\] ', '', formatted_ref)

            return formatted_ref

    # def get_language(self, text=""):
    #     nlp = spacy.load('en')
    #     nlp.add_pipe(Reference.language_detector)
    #     doc = nlp(text)

    #     return doc._.languages

    def log_error(self, e):
        print(e)
