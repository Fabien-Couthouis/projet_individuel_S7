from .contentExtraction import ContentExtraction


class ContentExtractionPDF(ContentExtraction):

    def __init__(self, url=""):
        self.url = url
        self.content = self.get_content()

    def get_content(self):
        return NotImplemented

    def get_author_name(self):
        return NotImplemented

    def get_title(self):
        return NotImplemented

    def get_publication_date(self):
        return NotImplemented
