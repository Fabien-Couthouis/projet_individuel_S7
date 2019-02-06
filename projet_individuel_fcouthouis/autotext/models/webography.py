import spacy
from .source import Source
from urlextract import URLExtract


class Webography():

    def __init__(self, raw_url_list):
        self.raw_url_list = raw_url_list
        self.structured_url_list = [""]

    def get_structurated_url_list(self):
        if self.structured_url_list == [""]:
            extractor = URLExtract()
            # Si raw_url_list ne contient pas d'url, renvoie [] (et pas [""])
            structured_url_list = extractor.find_urls(self.raw_url_list)

            # Suppression des occurences multiples et ajout dans la propriété
            self.structured_url_list = list(set(structured_url_list))

        return self.structured_url_list

    def generate(self, standard):
        return "I am the " + standard + " webography :)"
