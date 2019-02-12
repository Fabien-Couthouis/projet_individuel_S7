#inspred from https://www.crummy.com/software/BeautifulSoup/bs4/doc/#

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re


class ContentExtraction():

    def __init__(self, url=""):
        self.url = url

    def simple_get(self):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
        """
        try:
            with closing(get(self.url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    return None

        except RequestException as e:
            self.log_error(
                'Error during requests to {0} : {1}'.format(self.url, str(e)))
            return None

    def is_good_response(self, resp):
        """
        Returns True if the response seems to be HTML, False otherwise.
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)

    def log_error(self, e):
        print(e)

    def get_content(self):
        html_doc = self.simple_get()
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup

    def get_author(self):
        content = self.get_content()
        name = ""
        # Is one of them present in one of the tags below ?
        keyWords = ["by", "author"]

        for meta in content.find_all('meta'):
            # Tag meta 'name'
            if not (meta.get('name') is None):
                if any(keyWord in meta.get('name') for keyWord in keyWords):
                    name = meta.get('content')
                    break

            # Tag meta 'property'
            elif not (meta.get('property') is None):
                if any(keyWord in meta.get('property') for keyWord in keyWords):
                    name = meta.get('content')
                    break

        if name == "":
            self.log_error("No author found for this url : " + self.url)

        name = self.format_author_name(name)

        return name

    def format_author_name(self, name):
        '''Transform raw author name into formatted author name. For instance : http://www.nytimes/1550mireille-mathieu -> Mireille Mathieu'''
        # If link
        if "/" in name:
            name = re.search(r'[^/]+(?=/$|$)', name).group(0)

        if "-" in name:
            name = name.replace("-", " ")

        # Put uppercases on first letter of the name
        name = name.title()
        # Remove digits
        name = re.sub("\d+", "", name)
        # Remove "By"
        name = re.sub("[B|b]y", "", name)
        # Remove leading whitespaces
        name = name.lstrip()

        return name
