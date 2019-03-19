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

    def generate_articles(self):
        """Generate the list of articles in self.articles. Each article corresponds to one url."""
        structured_urls = self.get_structurated_urls_list()
        this = Webography.objects.filter(id=self.id)[0]
        for url in structured_urls:
            r = requests.get(url)
            content_type = r.headers['Content-Type'].lower()

            if 'application/pdf' in content_type:
                ref = ReferencePDF(url=url, webography=self)
                ref.save()
                this.referencepdf_set.add(ref)
            elif 'text/html' in content_type:
                ref = ReferenceWeb(url=url, webography=self)
                ref.save()
                this.referenceweb_set.add(ref)
            else:
                ref = None

    def get_bibtex_webography(self):
        bib_webography = []
        this = Webography.objects.get(id=self.id)
        # Parse the 2 reference_set
        for ref in this.referencepdf_set.all():
            bib_webography.append(ref.bibtex_reference)

        for ref in this.referenceweb_set.all():
            print(ref.bibtex_reference)
            bib_webography.append(ref.bibtex_reference)

        return bib_webography

    def get_formatted_webography(self, style='apa'):
        formatted_webography = []
        this = Webography.objects.get(id=self.id)

        # Parse the 2 reference_set
        for ref in this.referencepdf_set.all():
            print(ref)
            formatted_webography.append(ref.apa_reference)

        for ref in this.referenceweb_set.all():
            print(ref)
            formatted_webography.append(ref.apa_reference)

        return formatted_webography
