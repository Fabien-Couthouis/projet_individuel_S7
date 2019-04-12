#!/usr/bin/env python

"""
Library to query Semantic Scholar.
Call the method get_bib_from_title with a string which contains the title of the article.
This will return the bibtx citation of the article.
"""
import re
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

SEMANTIC_SCHOLAR_QUERY_URL = "https://www.semanticscholar.org/search?q="
SEMANTIC_SCHOLAR_API_URL = "http://api.semanticscholar.org/v1/paper/"


def get_bib_from_title(title):
    url = SEMANTIC_SCHOLAR_QUERY_URL + title
    options = Options()
    options.add_argument('-headless')
    browser = Firefox(firefox_options=options)

    browser.get(url)
    delay = 10  # seconds max until response
    try:
        # Wait for page loading
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'cite-button')))

        # Clic on button to get citation
        python_button = browser.find_elements_by_xpath(
            "//button[@class='icon-button cite-button' and @data-selenium-selector='cite-link']")[0]
        python_button.click()

        # Wait for content loading
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'formatted-citation')))

        # Retrieve bibtext citation
        soup = BeautifulSoup(browser.page_source, "html.parser")
        content = soup.find('cite', {'class': 'formatted-citation'})
        bib = content.text

        # Remove carriage return and double spaces
        bib = bib.replace("\n", "")
        bib = bib.replace("  ", "")

    except TimeoutException:
        print("Loading took too much time!")
        bib = "undefined"

    browser.quit()
    return bib
