# https://docs.python.org/2/library/unittest.html
from django.test import TestCase
from .models.source import Source
from .models.webography import Webography
from .models.contentExtractionSite import ContentExtractionSite
from .models.contentExtractionPDF import ContentExtractionPDF


# python manage.py test autotext.tests.SourceTest
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
        contentExtraction = ContentExtractionSite(url)
        content = contentExtraction.get_content()
        result_fr = Source().get_language(content)[0]
        self.assertEqual(result_fr, 'fr')


# python manage.py test autotext.tests.WebographyTest
class WebographyTest(TestCase):
    def test_get_structurated_url_list(self):
        raw_url_list = "https://docs.djangoproject.com/fr/2.1/topics/testing/overview/  https://github.com/django/djangoproject.com  http://notionsinformatique.free.fr/mac/ipad_guide_utilisateur.pdf  , https://stackoverflow.com/questions/32022024/django-code-organisation https://getbootstrap.com/docs/4.0/components/input-group/"
        webography = Webography(raw_url_list)
        expected = ["https://docs.djangoproject.com/fr/2.1/topics/testing/overview/", "https://github.com/django/djangoproject.com", "http://notionsinformatique.free.fr/mac/ipad_guide_utilisateur.pdf",
                    "https://stackoverflow.com/questions/32022024/django-code-organisation", "https://getbootstrap.com/docs/4.0/components/input-group/"]
        tested = webography.get_structurated_url_list()

        # On fait le test sur des sets puisque l'ordre dans lequel sont présentés les éléments n'importe pas ici
        self.assertEqual(set(tested), set(expected))


# python manage.py test autotext.tests.ContentExtractionSiteTest
class ContentExtractionSiteTest(TestCase):
    testUrl1 = "https://www.lemonde.fr/planete/article/2019/02/12/une-nouvelle-etude-suggere-un-effet-des-aliments-ultra-transformes-sur-la-sante_5422252_3244.html"
    testUrl2 = "https://www.nytimes.com/2019/02/11/world/europe/russia-polar-bears-emergency.html"
    testUrl3 = "https://www.liberation.fr/france/2019/02/12/patrick-drahi-laisse-les-cles-de-l-express-a-alain-weill_1708889"
    urls = [testUrl1, testUrl2, testUrl3]

    def test_get_author_name(self):
        expecteds = ["Pascale Santi", "Andrew E. Kramer", "Jerome Lefilliatre"]
        for url, expected in zip(ContentExtractionSiteTest().urls, expecteds):
            CE = ContentExtractionSite(url)
            tested = CE.get_author_name()
            self.assertEqual(tested, expected)

    def test_get_title(self):
        expecteds = ["Une nouvelle étude suggère un effet néfaste des aliments ultratransformés sur la santé",
                     "Polar Bears Have Invaded a Russian Outpost, and They’re Hungry", "Patrick Drahi laisse les clés de «l'Express» à Alain Weill"]

        for url, expected in zip(ContentExtractionSiteTest().urls, expecteds):
            CE = ContentExtractionSite(url)
            tested = CE.get_title()
            self.assertEqual(tested, expected)

    def test_get_publication_date(self):
        expecteds = ["2019-02-12T04:05:55+00:00",
                     "2019-02-11T21:44:17.000Z", "2019-02-12T15:25:03"]
        for url, expected in zip(ContentExtractionSiteTest().urls, expecteds):
            CE = ContentExtractionSite(url)
            tested = CE.get_publication_date()
            self.assertEqual(tested, expected)

# python manage.py test autotext.tests.ContentExtractionPDFTest
# A bit longer because of pdf files downloads


class ContentExtractionPDFTest(TestCase):
    testUrl1 = "https://arxiv.org/pdf/1706.05507.pdf"
    testUrl2 = "https://arxiv.org/pdf/1212.5701.pdf"
    testUrl3 = "https://nutritionj.biomedcentral.com/track/pdf/10.1186/s12937-019-0433-7"
    urls = [testUrl1, testUrl2, testUrl3]

    def test_get_author_name(self):
        expecteds = ["Mahesh Chandra Mukkamala, Matthias Hein",
                     "Matthew D. Zeiler", "Ali Alami"]
        for url, expected in zip(ContentExtractionPDFTest().urls, expecteds):
            CE = ContentExtractionPDF(url)
            tested = CE.get_author_name()
            print(tested)
            self.assertEqual(tested, expected)

    # def test_get_title(self):
    #     expecteds = ["Une nouvelle étude suggère un effet néfaste des aliments ultratransformés sur la santé",
    #                  "Polar Bears Have Invaded a Russian Outpost, and They’re Hungry", "Patrick Drahi laisse les clés de «l'Express» à Alain Weill"]

    #     for url, expected in zip(ContentExtractionPDFTest().urls, expecteds):
    #         CE = ContentExtractionPDF(url)
    #         tested = CE.get_title()
    #         self.assertEqual(tested, expected)

    # def test_get_publication_date(self):
    #     expecteds = ["2019-02-12T04:05:55+00:00",
    #                  "2019-02-11T21:44:17.000Z", "2019-02-12T15:25:03"]
    #     for url, expected in zip(ContentExtractionPDFTest().urls, expecteds):
    #         CE = ContentExtractionPDF(url)
    #         tested = CE.get_publication_date()
    #         self.assertEqual(tested, expected)
