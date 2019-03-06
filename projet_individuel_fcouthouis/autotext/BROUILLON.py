import urllib
import requests

url = "https://www.lemonde.fr/planete/article/2019/02/12/une-nouvelle-etude-suggere-un-effet-des-aliments-ultra-transformes-sur-la-sante_5422252_3244.html"
r = requests.head(url)
print(r.headers['content-type'])


url2 = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2225012/pdf/493.pdf"
r = requests.head(url2)
print(r.headers['content-type'])
