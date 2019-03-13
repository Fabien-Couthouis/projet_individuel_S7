from .reference import Reference
from requests import get
from requests.exceptions import RequestException
import PyPDF2
import tempfile
import pdftitle
import gscholar


class ReferencePDF(Reference):

    # def __init__(self):
    #     # super().__init__(url)
    #     self._get_content()

    def _get_content(self):
        try:
            response = get(self.url)
            temp = tempfile.NamedTemporaryFile()
            temp.write(response.content)
            # "After writing, the file handle must be “rewound” using seek() in order to read the data back from it." > error with pdfminer if not done
            temp.seek(0)

            self._content = temp

            return self._content

        except RequestException as e:
            self.log_error(
                'Error during requests to {0} : {1}'.format(self.url, str(e)))
            return None

    def get_metadata(self):
        inputPdf = PyPDF2.PdfFileReader(open(self._content.name, "rb"))
        metadata = inputPdf.getDocumentInfo()

        return metadata

    def get_bibtex_reference(self):
        # self._content.name gives the path to the self._content tempfile
        title = pdftitle.get_title(self._content.name)

        source = gscholar.query(title)

        if len(source) != 0:
            return source[0]
        else:
            return None
