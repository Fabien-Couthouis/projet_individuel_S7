import spacy
from .source import Source
import re


class Webography():

    def __init__(self, raw_url_list):
        self.raw_url_list = raw_url_list

    def get_structurated_url_list(self):
        structured_url_list = []
        return structured_url_list

    def generate(self, standard):
        return "I am the " + standard + " webography :)"
