from .article import Article
from requests import get
from requests.exceptions import RequestException
import PyPDF2
import tempfile
import pdftitle
import gscholar


class ArticlePDF(Article):

    def __init__(self, url=""):
        super().__init__(url)
        self.content = None
        self.get_content()

    def get_content(self):
        try:
            response = get(self.url)
            raw_data = response.content

            self.content = tempfile.NamedTemporaryFile()
            self.content.write(raw_data)

            return self.content

        except RequestException as e:
            self.log_error(
                'Error during requests to {0} : {1}'.format(self.url, str(e)))
            return None

    def get_metadata(self):
        inputPdf = PyPDF2.PdfFileReader(open(self.content.name, "rb"))
        metadata = inputPdf.getDocumentInfo()

        return metadata

    def get_bibtex_reference(self):
        title = pdftitle.get_title(self.content.name)
        source = gscholar.query(title)[0]
        # self.content.close()
        return source
