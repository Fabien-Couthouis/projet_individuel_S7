from .referencePDF import ReferencePDF
from .referenceWeb import ReferenceWeb
from urlextract import URLExtract
import requests


class Webography():

    def __init__(self, raw_urls_string):
        self.raw_urls = raw_urls_string
        self.articles = []

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
        for url in structured_urls:
            r = requests.get(url)
            content_type = r.headers['Content-Type'].lower()

            if 'application/pdf' in content_type:
                article = ReferencePDF(url)
            elif 'text/html' in content_type:
                article = ReferenceWeb(url)
            else:
                article = None

            self.articles.append(article)

    def get_bibtex_webography(self):
        bib_webography = []
        for article in self.articles:
            bib_ref = article.get_bibtex_reference()
            bib_webography.append(bib_ref)

        return bib_webography

    def get_formatted_webography(self, style='apa'):
        formatted_webography = []
        for article in self.articles:
            formatted_ref = article.get_formatted_reference(style)
            formatted_webography.append(formatted_ref)

        return formatted_webography
