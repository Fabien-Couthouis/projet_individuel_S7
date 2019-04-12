from .reference import Reference
from requests import get
from requests.exceptions import RequestException
import PyPDF2
import tempfile
import pdftitle
import gscholar
from ..Helpers import sscholar


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

    def _get_bibtex_reference(self):
        content = self._retrieve_content()
        title = pdftitle.get_title_from_file(content.name)

        # SemanticScholar
        bibref = sscholar.get_bib_from_title(title)

        # Try Gscholar if not found on semanticscholar
        if bibref == "undefined":
            sources = gscholar.query(title)
            if sources:
                bibref = sources[0]

        return bibref
