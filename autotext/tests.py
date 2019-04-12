# https://docs.python.org/2/library/unittest.html
from django.test import TestCase
from .models.webography import Webography
from .models.referenceWeb import ReferenceWeb
from .models.referencePDF import ReferencePDF


# python manage.py test autotext.tests.WebographyTest
class WebographyTest(TestCase):
    def test_get_structurated_url_list(self):
        raw_url_list = "https://docs.djangoproject.com/fr/2.1/topics/testing/overview/  https://github.com/django/djangoproject.com  http://notionsinformatique.free.fr/mac/ipad_guide_utilisateur.pdf  , https://stackoverflow.com/questions/32022024/django-code-organisation https://getbootstrap.com/docs/4.0/components/input-group/"
        webography = Webography()
        expected = ["https://docs.djangoproject.com/fr/2.1/topics/testing/overview/", "https://github.com/django/djangoproject.com", "http://notionsinformatique.free.fr/mac/ipad_guide_utilisateur.pdf",
                    "https://stackoverflow.com/questions/32022024/django-code-organisation", "https://getbootstrap.com/docs/4.0/components/input-group/"]
        tested = webography.get_structurated_urls(raw_url_list)

        # Order does not matter here so we use sets instead of lists
        self.assertEqual(set(tested), set(expected))


# python manage.py test autotext.tests.ArticleSiteTest
class ArticleSiteTest(TestCase):
    testUrl1 = "https://www.lemonde.fr/planete/article/2019/02/12/une-nouvelle-etude-suggere-un-effet-des-aliments-ultra-transformes-sur-la-sante_5422252_3244.html"
    testUrl2 = "https://www.nytimes.com/2019/02/11/world/europe/russia-polar-bears-emergency.html"
    testUrl3 = "https://www.liberation.fr/france/2019/02/12/patrick-drahi-laisse-les-cles-de-l-express-a-alain-weill_1708889"
    urls = [testUrl1, testUrl2, testUrl3]

    def test_get_author_name(self):
        expecteds = ["Pascale Santi", "Andrew E. Kramer", "Jerome Lefilliatre"]
        for url, expected in zip(ArticleSiteTest().urls, expecteds):
            article = ReferenceWeb(url)
            content = article._retrieve_content()
            tested = article.get_author(content)
            self.assertEqual(tested, expected)

    def test_get_title(self):
        expecteds = ["Une nouvelle étude suggère un effet néfaste des aliments ultratransformés sur la santé",
                     "Polar Bears Have Invaded a Russian Outpost, and They’re Hungry", "Patrick Drahi laisse les clés de «l'Express» à Alain Weill"]

        for url, expected in zip(ArticleSiteTest().urls, expecteds):
            article = ReferenceWeb(url)
            content = article._retrieve_content
            tested = article.get_title(content)
            self.assertEqual(tested, expected)

    def test_get_publication_date(self):
        expecteds = ["2019-02-12T04:05:55+00:00",
                     "2019-02-11T21:44:17.000Z", "2019-02-12T15:25:03"]
        for url, expected in zip(ArticleSiteTest().urls, expecteds):
            article = ReferenceWeb(url)
            content = article._retrieve_content
            tested = article.get_publication_date(content)
            self.assertEqual(tested, expected)

    # No error test
    def test_get_bibtex_reference(self):
        article = ReferenceWeb(ArticleSiteTest().testUrl1)
        tested = article.bibtex_reference
        print("test_get_bibtex_reference : " + tested)

    def test_get_formatted_reference(self):
        article = ReferenceWeb(ArticleSiteTest().testUrl1)
        expected = "Pascale Santi, P. S. (2019, 12 février). Une nouvelle étude suggère un effet néfaste des aliments ultratransformés sur la santé. Récupéré 5 mars, 2019, de https://www.lemonde.fr/planete/article/2019/02/12/une-nouvelle-etude-suggere-un-effet-des-aliments-ultra-transformes-sur-la-sante_5422252_3244.html"
        tested = article.apa_reference

        self.assertEqual(tested, expected)

# python manage.py test autotext.tests.ArticlePDFTest
# A bit longer because of pdf files downloads


class ArticlePDFTest(TestCase):
    testUrl1 = "https://arxiv.org/pdf/1706.05507.pdf"
    testUrl2 = "https://arxiv.org/pdf/1212.5701.pdf"
    # no metadata
    testUrl3 = "https://nutritionj.biomedcentral.com/track/pdf/10.1186/s12937-019-0433-7"
    testUrl4 = "https://arxiv.org/pdf/1902.06865.pdf"
    testUrl5 = "https://arxiv.org/pdf/1711.08416.pdf"
    testUrl6 = "http://ciir.cs.umass.edu/pubfiles/ir-329.pdf"
    webography = Webography()
    webography.save()

    urls = [testUrl1, testUrl2, testUrl3, testUrl4, testUrl5, testUrl6]

    def test_get_bibtext_reference(self):
        article = ReferencePDF(webography_id=ArticlePDFTest().webography.id,
                               url=ArticlePDFTest().testUrl1)
        print(article.url)

        expected = '@article{alami2019factors, \ntitle = {Factors that influence dietary behavior toward iron and vitamin D consumption based on the theory of planned behavior in Iranian adolescent girls}, \n  author = {Alami, Ali and Sany, Seyedeh Belin Tavakoly and Lael-Monfared, Elaheh and Ferns, Gordon A and Tatari, Maryam and Hosseini, Zahra and Jafari, Alireza}, \n  journal = {Nutrition journal}, \n  volume = {18}, \n  number = {1}, \n  pages = {8}, \n  year = {2019}, \n  publisher = {BioMed Central}\n}\n'
        self.assertEqual(article.bibtex_reference, expected)

    def test_get_apaSource(self):
        article = ReferencePDF(url=ArticlePDFTest().testUrl3)
        expected = "[Alami et al., 2019] Alami, A., Sany, S. B. T., Lael-Monfared, E., Ferns, G. A., Tatari, M., Hosseini, Z., & Jafari, A. (2019). Factors that influence dietary behavior toward iron and vitamin d consumption based on the theory of planned behavior in iranian adolescent girls. Nutrition journal, 18(1), 8."
        print(expected)
        print(article.apa_reference)
        self.assertEqual(
            article.apa_reference, expected)
