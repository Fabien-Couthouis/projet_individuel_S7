# %%
from requests import get
from IPython.display import display
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

# %%
url = "http://fr.python-requests.org/en/latest/user/quickstart.html#creer-une-requete"
r = get(url)
# display(r.text)
print(r.text)


# %%
# url = "http://www.leparisien.fr/info-paris-ile-de-france-oise/transports/neige-en-ile-de-france-circulation-delicate-sur-les-routes-les-bus-a-l-arret-30-01-2019-7999950.php"
# url = "https://www.nytimes.com/2019/01/29/us/politics/kim-jong-trump.html"
url = "https://www.lemonde.fr/international/article/2019/01/30/qu-est-ce-que-le-backstop-irlandais-au-c-ur-du-rejet-de-l-accord-sur-le-brexit_5416730_3210.html"


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


raw_html = simple_get(url)
html = BeautifulSoup(raw_html, 'html.parser')
for p in html.select('p'):
    print(p.text)
