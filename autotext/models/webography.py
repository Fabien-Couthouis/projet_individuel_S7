from urlextract import URLExtract
import requests
from django.contrib.auth import get_user_model
from django.db import models
from .referenceWeb import ReferenceWeb
from .referencePDF import ReferencePDF


class Webography(models.Model):
    # raw_urls = models.TextField(null=True)
    _name = models.TextField(null=True, default="")
    user = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE, related_name="user_references")

    def __str__(self):
        return str(self.name)

    @property
    def name(self):
        if self._name == "" or self._name == None:
            return "Webography n°" + str(self.id)
        else:
            return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def get_structurated_urls(self, raw_urls):
        """Get a structurated list of urls from the raw_urls string"""
        extractor = URLExtract()
        # Return [] if no url is present in raw_url_list(and not [""])
        structured_urls = extractor.find_urls(raw_urls)

        # Multiple occurence suppression by passing structured_url_list into a set
        structured_urls = list(set(structured_urls))

        return structured_urls

    def add_reference(self, url, bibtex_reference=None, apa_reference=None):
        ''' Automatically add a reference in this webography.'''
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

    def add_refererences_from_urls(self, raw_urls):
        """Generate the list of references from a list of urls. Each article corresponds to one url."""
        structured_urls = self.get_structurated_urls(raw_urls)
        for url in structured_urls:
            self.add_reference(url)

    def get_bibtex_webography(self):
        bib_webography = []
        # Parse the 2 reference_set
        for ref in self.referencepdf_set.all():
            bib_webography.append(ref.bibtex_reference.replace("\n", ""))

        for ref in self.referenceweb_set.all():
            bib_webography.append(ref.bibtex_reference.replace("\n", ""))

        return bib_webography

    def get_formatted_webography(self):
        '''Get the webography in the apa format'''
        formatted_webography = []
        this = Webography.objects.get(id=self.id)

        # Parse the 2 reference_set
        for ref in this.referencepdf_set.all():
            formatted_webography.append(ref.apa_reference)

        for ref in this.referenceweb_set.all():
            formatted_webography.append(ref.apa_reference)

        return formatted_webography
