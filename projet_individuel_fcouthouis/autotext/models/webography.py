from django.db import models
from urlextract import URLExtract
import requests
from django.contrib.auth import get_user_model

from .referenceWeb import ReferenceWeb
from .referencePDF import ReferencePDF


class Webography(models.Model):
    class Meta:
        db_table = 'Webography'

    _raw_urls = models.TextField(null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_references")

    # references = models.ManyToManyField(Reference)

    # def __init__(self, _raw_urls_string):
    #     self._raw_urls = _raw_urls_string
    #     self.articles = []

    def get_structurated_urls_list(self):
        """Get a structurated list of urls from the _raw_urls string"""
        extractor = URLExtract()
        # Return [] if no url is present in raw_url_list(and not [""])
        structured_urls = extractor.find_urls(self._raw_urls)

        # Multiple occurence suppression by passing structured_url_list into a set
        structured_urls = list(set(structured_urls))

        return structured_urls

    def generate_articles(self):
        """Generate the list of articles in self.articles. Each article corresponds to one url."""
        structured_urls = self.get_structurated_urls_list()
        for url in structured_urls:
            r = requests.get(url)
            content_type = r.headers['Content-Type'].lower()

            if 'application/pdf' in content_type:
                ref = ReferencePDF(url)
            elif 'text/html' in content_type:
                ref = ReferenceWeb(url)
            else:
                ref = None

            # self.webography_references.add(ref)
            Webography.objects.get(self).webography_references.add(ref)
            # Reference.objects.filter().add(ref)

    def get_bibtex_webography(self):
        bib_webography = []
        # for ref in self.
        #     bib_ref = ref.get_bibtex_reference()
        #     bib_webography.append(bib_ref)

        return bib_webography

    def get_formatted_webography(self, style='apa'):
        formatted_webography = []
        # for ref in self.references:
        #     formatted_ref = ref.get_formatted_reference(style)
        #     formatted_webography.append(formatted_ref)

        return formatted_webography
