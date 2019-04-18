from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from .reference import Reference
import re
from datetime import datetime


class ReferenceWeb(Reference):

    def _retrieve_content(self):
        """
        Attempts to get the soup at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content (soup), otherwise return None. Inspired from https://www.crummy.com/software/BeautifulSoup/bs4/doc/#
        """

        try:
            with closing(get(self.url, stream=True)) as resp:
                if self._is_good_response(resp):
                    raw_content = resp.content
                    soup = BeautifulSoup(raw_content, 'html.parser')
                    return soup

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

    def get_author(self, soup):
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

        name = self._get_data(soup, searches, element_types)

        # Author name not found
        if name == "":
            self.log_error("No author found for this url : " + self.url)
            return name

        # Return formatted
        return self._format_author_name(name)

    def _format_author_name(self, name):
        '''Transform raw author name into formatted author name. For instance : http://www.nytimes/1550mireille-mathieu -> Mireille Mathieu'''
        # If sentence
        if name.count(" ") > 5:
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
        name = re.sub("[B|b]y", "", name)
        # Translate "et"
        name = re.sub("[E|e]t", "and", name)
        # Remove leading whitespaces and newlines
        name = name.lstrip()

        return name

    def get_title(self, soup):
        searches = [
            {'property': 'og:title'}
        ]
        element_types = ['content']

        title = self._get_data(soup, searches, element_types)

        if title == "":
            self.log_error("No title found for this url : " + self.url)

        return title

    def get_publication_date(self, soup):
        searches = [
            {'property': re.compile(r"published")},
            {'property': re.compile(r"publication")},
            {'itemprop': re.compile(r"published")},
            {'class': re.compile(r"date")}
        ]

        element_types = ['content', 'datetime']

        pub_date = self._get_data(soup, searches, element_types)
        # Not found
        if pub_date == "":
            self.log_error("No date found for this url : " + self.url)
            return ""

        # Return formatted
        try:
            return self._format_publication_date(pub_date)
        except:
            return ""

    def _format_publication_date(self, string_iso):
        """Convert string publication date into an exploitable datetime. """
        # We need to remove the ":" because '%z' in strptime doesnt requiere any ":" so that we do not get any error.
        # See https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior for more info.
        string_iso = string_iso.replace(":", "")
        # Remove utc info and hours, sometimes the format differs and we do not really care about hours
        string_iso = string_iso.split("T")[0]
        dt = datetime.strptime(string_iso, "%Y-%m-%d")
        return dt

    def _get_data(self, soup, searches, element_types):
        ''' Retrieve soup from searches, in the given order '''
        print(type(soup))
        for search in searches:
            element = soup.find(attrs=search)
            if (element is not None):
                for element_type in element_types:
                    try:
                        print(element[element_type])
                        return element[element_type]
                    except KeyError:
                        return element.text

                        # # If last alement
                        # if element_type == element_types[-1] and search == searches[-1]:
                        #     if element.text:
                        #         print(element.text)

                        #         return element.text

        # No element found : return empty string
        return ''

    def _get_bibtex_reference(self):
        print("TRY TO GET BIBTEX REFERENCE")
        soup = self._retrieve_content()
        print("get author")
        author = self.get_author(soup)
        print("get title")

        title = self.get_title(soup)
        print("get pubate")

        pubDate = self.get_publication_date(soup)
        # Triple curly brackets because we want the info to be in this format in the string : {Author Name}
        bibRef = ("@misc{{website, author = {{{author}}}, title = {{{title}}}, url = {{{url}}}, year={{{year}}}, month={{{month}}}, note = {{{note}}}}}"
                  ).format(author=author, title=title, url=self.url, year=pubDate.strftime("%Y") if (pubDate != "") else "", month=pubDate.strftime("%B") if (pubDate != "") else "", note=("Online, accessed " + datetime.now().strftime('%d %B %Y')))

        return bibRef.rstrip()
