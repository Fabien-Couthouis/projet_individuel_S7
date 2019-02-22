from .contentExtraction import ContentExtraction
from requests import get
from requests.exceptions import RequestException
import PyPDF2


class ContentExtractionPDF(ContentExtraction):

    def __init__(self, url=""):
        self.url = url
        self.content = None
        self.get_content()

    def get_content(self):
        try:
            response = get(self.url)
            my_raw_data = response.content

            with open("temp.pdf", 'wb') as my_data:
                my_data.write(my_raw_data)

            open_pdf_file = open("temp.pdf", 'rb')
            self.content = PyPDF2.PdfFileReader(open_pdf_file)
            return self.content

        except RequestException as e:
            self.log_error(
                'Error during requests to {0} : {1}'.format(self.url, str(e)))
            return None

    def get_author_name(self):
        try:
            info = self.content.getDocumentInfo()
            return info['/Author']
            # return self.content.getDocumentInfo().author

        except ReferenceError as e:
            self.log_error(
                'Error while getting author info to {0} : {1}'.format(self.url, str(e)))
            return None

    def get_title(self):
        try:
            info = self.content.getDocumentInfo()
            return info['/Title']

        except ReferenceError as e:
            self.log_error(
                'Error while getting title info to {0} : {1}'.format(self.url, str(e)))
            return None

    def get_publication_date(self):
        try:
            info = self.content.getDocumentInfo()
            return info['/CreationDate']

        except ReferenceError as e:
            self.log_error(
                'Error while getting publication date info to {0} : {1}'.format(self.url, str(e)))
            return None
