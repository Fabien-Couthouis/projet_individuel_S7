from django.db import models
from urlextract import URLExtract
import requests
from django.contrib.auth import get_user_model

from .referenceWeb import ReferenceWeb
from .referencePDF import ReferencePDF
from pprint import pprint


class Webography(models.Model):
    raw_urls = models.TextField(null=True)
    user = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE, related_name="user_references")

    # references = models.ManyToManyField(Reference)

    # def __init__(self, _raw_urls_string):
    #     self.raw_urls = _raw_urls_string
    #     self.articles = []

    def get_structurated_urls_list(self):
        """Get a structurated list of urls from the raw_urls string"""
        extractor = URLExtract()
        # Return [] if no url is present in raw_url_list(and not [""])
        structured_urls = extractor.find_urls(self.raw_urls)

        # Multiple occurence suppression by passing structured_url_list into a set
        structured_urls = list(set(structured_urls))

        return structured_urls

    def add_reference(self, url, bibtex_reference=None, apa_reference=None):
        r = requests.get(url)
        content_type = r.headers['Content-Type'].lower()
        if 'application/pdf' in content_type:
            ref = ReferencePDF(url=url, bibtex_reference=bibtex_reference,
                               apa_reference=apa_reference, webography=self)
            ref.save()
            self.referencepdf_set.add(ref)
        elif 'text/html' in content_type:
            ref = ReferenceWeb(url=url, bibtex_reference=bibtex_reference,
                               apa_reference=apa_reference, webography=self)
            ref.save()
            self.referenceweb_set.add(ref)
        else:
            raise ValueError

    def generate_articles(self):
        """Generate the list of articles in self.articles. Each article corresponds to one url."""
        structured_urls = self.get_structurated_urls_list()
        for url in structured_urls:
            self.add_reference(url)

    def get_bibtex_webography(self):
        bib_webography = []
        # Parse the 2 reference_set
        for ref in self.referencepdf_set.all():
            bib_webography.append(ref.bibtex_reference)

        for ref in self.referenceweb_set.all():
            bib_webography.append(ref.bibtex_reference)

        return bib_webography

    def get_formatted_webography(self, style='apa'):
        formatted_webography = []
        this = Webography.objects.get(id=self.id)

        # Parse the 2 reference_set
        for ref in this.referencepdf_set.all():
            formatted_webography.append(ref.apa_reference)

        for ref in this.referenceweb_set.all():
            formatted_webography.append(ref.apa_reference)

        return formatted_webography
