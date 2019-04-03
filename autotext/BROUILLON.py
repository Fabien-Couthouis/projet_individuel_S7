import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Alraedy implemented
url = "https://docs.unity3d.com/Manual/UnityBasics.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


regex = re.compile("(\d{4})[-|.](\d{1,})-(\d{1,})T")
for item in soup.find_all(text=regex):
    # group(0) returns thefull matched text
    matched = regex.search(item).group(0)

matched = matched.replace(".", "-")
print(matched)
matched = "2018-03-02T"
dt = datetime.strptime(matched, "%Y-%m-%dT")

print(dt)
