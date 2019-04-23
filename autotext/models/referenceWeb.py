import re
from datetime import datetime
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from .reference import Reference

DEBUG = True


class ReferenceWeb(Reference):

    def _retrieve_content(self):
        """
        Attempts to get the soup at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content (soup), otherwise return None.
        """
        try:
            response = get(self.url, stream=True)
            soup = BeautifulSoup(response.content.decode(
                'utf-8', 'ignore'), 'html.parser')
            return soup

        except RequestException as e:
            self._log_error(
                'Error during requests to {0} : {1}'.format(self.url, str(e)))
            return None

    def get_author(self, soup):
        '''Retrieve author name in html'''
        if DEBUG:
            self._log_error("Getting author ...")

        searches = [
            {'name': re.compile(r"author-name")},
            {'property': re.compile(r"author-name")},
            {'class': re.compile(r"author-name")},
            {'name': re.compile(r"author")},
            {'property': re.compile(r"author")},
            {'class': re.compile(r"author")},
            {'name': re.compile(r"by")},
            {'content': re.compile(r"by")},
        ]
        element_types = ['content']

        try:
            name = self._get_data(soup, searches, element_types)
            return self._format_author(name)
        except ValueError as e:
            if DEBUG:
                self._log_error(
                    "No author found for reference : {0}.\nError : {1}".format(str(self), str(e)))
            return ""

    def _format_author(self, name):
        '''Transform raw author name into formatted author name. For instance : http://www.nytimes/1550mireille-mathieu -> Mireille Mathieu'''
        # If sentence
        if name.count(' ') > 5:
            regex = re.search('(by|with|par|avec)(.*?)(,|.),', name)
            if regex:
                name = regex.group(2)

        # If link
        elif "/" in name:
            name = re.search(r'[^/]+(?=/$|$)', name).group(0)

        if "-" in name:
            name = name.replace("-", " ")

        # Put uppercases on first letter of the name
        name = name.title()
        # Remove digits
        name = re.sub(r"\d+", "", name)
        # Remove "By"
        name = re.sub("[B|b]y ", "", name)
        # Translate "et"
        name = re.sub(" [E|e]t ", " and ", name)
        # Remove leading whitespaces and newlines
        name = name.lstrip()

        return name

    def get_title(self, soup):
        '''Retrieve reference title in html'''
        if DEBUG:
            self._log_error("Getting title ...")

        searches = [
            {'property': 'og:title'}
        ]
        element_types = ['content']

        try:
            title = self._get_data(soup, searches, element_types)
            return title

        except ValueError as e:
            if DEBUG:
                self._log_error(
                    "No title found for reference : {0}.\nError : {1}".format(str(self), str(e)))
            return ""

    def get_publication_date(self, soup):
        self._log_error("Getting publication date ...")
        searches = [
            {'property': re.compile(r"published")},
            {'property': re.compile(r"publication")},
            {'itemprop': re.compile(r"published")},
            {'class': re.compile(r"date")}
        ]

        element_types = ['content', 'datetime']

        try:
            pub_date = self._get_data(soup, searches, element_types)
            # Return formatted
            return self._format_publication_date(pub_date)

        except ValueError as e:
            if DEBUG:
                self._log_error(
                    "No date found for this url : {0}.\nError : {1}".format(str(self), str(e)))
            return ""

    def _format_publication_date(self, date_iso):
        """Convert string publication date into an exploitable datetime. """
        # We need to remove the ":" because '%z' in strptime doesnt requiere any ":" so that we do not get any error.
        # See https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior for more info.
        date_iso = date_iso.replace(":", "")
        # Remove utc info and hours, sometimes the format differs and we do not really care about hours
        date_iso = date_iso.split("T")[0]
        dt = datetime.strptime(date_iso, "%Y-%m-%d")
        return dt

    def _get_data(self, soup, searches, element_types):
        ''' Retrieve soup from searches, in the given order '''
        for search in searches:
            # print(search)
            element = soup.find(attrs=search)
            if element is not None:
                for element_type in element_types:
                    try:
                        return element[element_type]
                    except KeyError:
                        return element.text

        # No element found : return empty string
        return ""

    def _get_bibtex_reference(self):
        if DEBUG:
            self._log_error("Getting bibtex reference ...")
        soup = self._retrieve_content()

        author = self.get_author(soup)
        title = self.get_title(soup)
        pubDate = self.get_publication_date(soup)

        # Triple curly brackets because we want the info to be in this format in the string : {Author Name}
        bibRef = ("@misc{{website, author = {{{author}}}, title = {{{title}}}, url = {{{url}}}, year={{{year}}}, month={{{month}}}, note = {{{note}}}}}"
                  ).format(author=author, title=title,
                           url=self.url, year=pubDate.strftime(
                               "%Y") if (pubDate != "") else "",
                           month=pubDate.strftime("%B") if (
                               pubDate != "") else "",
                           note=("Online, accessed " + datetime.now().strftime('%d %B %Y')))

        return bibRef.rstrip()
