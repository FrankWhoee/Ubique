import requests

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "query",
    "format": "json",
    "list": "allcategories",
    "acfrom": "15th-century caliphs"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

CATEGORIES = DATA["query"]["allcategories"]

for cat in CATEGORIES:
    print(cat["*"])