import requests
import json

from bs4 import BeautifulSoup

from flask import Flask, request
app = Flask(__name__)

@app.route('/search_wikipedia')
def search_wikipedia():
    query = request.args.get('q')

    zimply_request = requests.get('http://localhost:9454/?q={}'.format(query))
    soup = BeautifulSoup(zimply_request.content)

    links = {}

    for link in soup.findAll('a'):
        href = link.get('href')

        links[link.text] = "/get_wikipedia?article={}".format(href)

    return json.dumps(links)

@app.route('/get_wikipedia')
def get_wikipedia():
    article = request.args.get('article')

    zimply_article_request = requests.get('http://localhost:9454/{}'.format(article))

    return zimply_article_request.content
