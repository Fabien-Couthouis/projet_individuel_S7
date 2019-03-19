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

    def _retrieve_content(self):
        """
        Retrieve content (pdf file) on the web, if not already done.
        """
        if self._content is None:
            try:
                response = get(self.url)
                temp = tempfile.NamedTemporaryFile()
                temp.write(response.content)
                # "After writing, the file handle must be “rewound” using seek() in order to read the data back from it." > error with pdfminer if not done
                temp.seek(0)

                self._content = temp

            except RequestException as e:
                self.log_error(
                    'Error during requests to {0} : {1}'.format(self.url, str(e)))
                return None

        return self._content

    def get_metadata(self):
        inputPdf = PyPDF2.PdfFileReader(open(self._content.name, "rb"))
        metadata = inputPdf.getDocumentInfo()

        return metadata

    def get_bibtex_reference(self):
        self._retrieve_content()
        # Set _bibtex_reference value if null
        if self._bibtex_reference is None:
            # self._content.name gives the path to the self._content tempfile
            print(self._content.name)

            title = pdftitle.get_title(self._content.name)

            source = gscholar.query(title)

            if source:
                self._bibtex_reference = source[0]

        return self._bibtex_reference
