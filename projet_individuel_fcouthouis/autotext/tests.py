# https://docs.python.org/2/library/unittest.html
from django.test import TestCase
from .models.source import Source
from .models.webography import Webography
from .models.contentExtraction import ContentExtraction


class SourceTest(TestCase):

    def test_get_language(self):
        text_fr = "Bonjour les amis."
        text_de = "Hallo Freunde."
        text_es = "Buenos dias amigos."

        source = Source()
        result_fr = source.get_language(text_fr)[0]
        result_de = source.get_language(text_de)[0]
        result_sp = source.get_language(text_es)[0]

        self.assertEqual(result_fr, 'fr')
        self.assertEqual(result_de, 'de')
        self.assertEqual(result_sp, 'es')

    def test_get_language_on_article(self):
        url = "https://www.lemonde.fr/international/article/2019/01/30/qu-est-ce-que-le-backstop-irlandais-au-c-ur-du-rejet-de-l-accord-sur-le-brexit_5416730_3210.html"
        contentExtraction = ContentExtraction()
        content = contentExtraction.get_content(url)
        result_fr = Source().get_language(content)[0]
        self.assertEqual(result_fr, 'fr')


class WebographyTest(TestCase):
    def test_get_structurated_url_list(self):
        raw_url_list = "https://docs.djangoproject.com/fr/2.1/topics/testing/overview/    https://github.com/django/djangoproject.com,https://stackoverflow.com/questions/32022024/django-code-organisation https://getbootstrap.com/docs/4.0/components/input-group/https://docs.djangoproject.com/fr/2.1/topics/testing/overview/"
        webography = Webography(raw_url_list)
        expected = ["https://docs.djangoproject.com/fr/2.1/topics/testing/overview/", "https://github.com/django/djangoproject.com",
                    "https://stackoverflow.com/questions/32022024/django-code-organisation", "https://getbootstrap.com/docs/4.0/components/input-group/"]

        self.assertEqual(webography.get_structurated_url_list(), expected)
