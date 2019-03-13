
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from .reference import Reference
import re
from datetime import datetime


class ReferenceWeb(Reference):

    # def __init__(self, url=""):
    #     super().__init__(url)
    #     self._content = self._get_content()

    def _get_content(self):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None. Inspired from https://www.crummy.com/software/BeautifulSoup/bs4/doc/#
        """
        try:
            with closing(get(self.url, stream=True)) as resp:
                if self._is_good_response(resp):
                    rawContent = resp.content
                    formattedContent = BeautifulSoup(
                        rawContent, 'html.parser')

                    self._content = formattedContent

                    return self._content
                else:
                    return None

        except RequestException as e:
            self.log_error(
                'Error during requests to {0} : {1}'.format(self.url, str(e)))
            return None

    def _is_good_response(self, resp):
        """
        Returns True if the response seems to be HTML, False otherwise.
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)

    def get_author_name(self):
        # Is one of them present in one of the elements below ?
        keyWords = ["by", "author"]
        metas = self._content.find_all('meta')
        elementsToSearch = ['name', 'property']

        name = self._get_meta_content(metas, elementsToSearch, keyWords)

        if name == "":
            self.log_error("No author found for this url : " + self.url)

        formattedName = self._format_author_name(name)

        return formattedName

    def _format_author_name(self, name):
        '''Transform raw author name into formatted author name. For instance : http://www.nytimes/1550mireille-mathieu -> Mireille Mathieu'''
        # If link
        if "/" in name:
            name = re.search(r'[^/]+(?=/$|$)', name).group(0)

        if "-" in name:
            name = name.replace("-", " ")

        # Put uppercases on first letter of the name
        name = name.title()
        # Remove digits
        name = re.sub(r"\d+", "", name)
        # Remove "By"
        name = re.sub("[B|b]y", "", name)
        # Remove leading whitespaces
        name = name.lstrip()

        return name

    def get_title(self):
        # Is one of them present in one of the elements below ?
        keyWords = ["title"]
        metas = self._content.find_all('meta')
        elementsToSearch = ['property']

        title = self._get_meta_content(metas, elementsToSearch, keyWords)

        if title == "":
            self.log_error("No title found for this url : " + self.url)

        return title

    def get_publication_date(self):
        keyWords = ["published"]
        metas = self._content.find_all('meta')
        elementsToSearch = ['property']

        publicationDate = self._get_meta_content(
            metas, elementsToSearch, keyWords)

        # Convert pubdate from string to datetime
        formattedPublicationDate = self._format_publication_date(
            publicationDate)

        if formattedPublicationDate == "":
            self.log_error("No date found for this url : " + self.url)

        return formattedPublicationDate

    def _format_publication_date(self, isoStringPubDate):
        """Convert string publication date into an exploitable datetime. """
        # We need to remove the ":" because '%z' in strptime doesnt requiere any ":" so that we do not get any error.
        # See https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior for more info.
        isoStringPubDate = isoStringPubDate.replace(":", "")
        # Remove utc info, sometimes the format differs and we do not care about hours
        isoStringPubDate = isoStringPubDate[:17]
        print(isoStringPubDate)
        dt = datetime.strptime(isoStringPubDate, "%Y-%m-%dT%H%M%S")
        return dt

    def _get_meta_content(self, metas, elementsToSearch, keyWords):
        """
        Use beautifulsoup to get content corresponding to the keywords in the given element, parsing meta tags into the htlm doc.

        Arguments:
            metas -- List of all meta tags in the html document.
            elementsToSearch -- List of all elements in the meta tag wherein we want a keyword to be.
            keyWords -- List of keywords to search in the referenced elements.
     """
        i = 0
        metaContent = ""

        while (metaContent == "" and i < len(metas)):
            meta = metas[i]

            for element in elementsToSearch:
                if not (meta.get(element) is None):
                    if any(keyWord in meta.get(element) for keyWord in keyWords):
                        metaContent = meta.get('content')
                        # metaContent found : we can break the for
                        break

            # No metaContent found : iterate on the next <meta> tag
            i += 1

        return metaContent

    def get_bibtex_reference(self):
        author = self.get_author_name()
        title = self.get_title()
        pubDate = self.get_publication_date()
        # Triple curly brackets because we want the info to be in this format in the string : {Author Name}
        bibRef = ("@misc{{website, author = {{{author}}}, title = {{{title}}}, url = {{{url}}}, year={{{year}}}, month={{{month}}}, note = {{{note}}}}}"
                  ).format(author=author,
                           title=title,
                           url=self.url,
                           year=pubDate.strftime("%Y"),
                           month=pubDate.strftime("%B"),
                           note=("Online, accessed " + datetime.now().strftime('%d %B %Y')))
        return bibRef
