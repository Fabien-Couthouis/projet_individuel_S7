from .reference import Reference
from requests import get
from requests.exceptions import RequestException
import PyPDF2
import tempfile
import pdftitle
import gscholar


class ReferencePDF(Reference):
    def _retrieve_content(self):
        """
        Retrieve content (pdf file) on the web, if not already done.
        """
        try:
            response = get(self.url)
            temp = tempfile.NamedTemporaryFile()
            temp.write(response.content)
            # "After writing, the file handle must be “rewound” using seek() in order to read the data back from it." > error with pdfminer if not done
            temp.seek(0)

            content = temp

        except RequestException as e:
            self.log_error(
                'Error during requests to {0} : {1}'.format(self.url, str(e)))
            return None

        return content

    # def get_metadata(self):
    #     inputPdf = PyPDF2.PdfFileReader(open(self.content.name, "rb"))
    #     metadata = inputPdf.getDocumentInfo()

    #     return metadata

    def _get_bibtex_reference(self):
        content = self._retrieve_content()
        title = pdftitle.get_title_from_file(content.name)
        source = gscholar.query(title)

        if source:
            bibref = source[0]
        else:
            bibref = "undefined"

        return bibref
