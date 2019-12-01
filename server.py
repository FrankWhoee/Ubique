import requests
import json

from bs4 import BeautifulSoup

from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/search_wikipedia')
def search_wikipedia():
    query = request.args.get('q')

    zimply_request = requests.get('http://localhost:9454/?q={}'.format(query))
    soup = BeautifulSoup(zimply_request.content)

    links = {}

    for link in soup.findAll('a'):
        href = link.get('href')

        links[link.text] = "/{}".format(href)

    return json.dumps(links)

@app.route('/<article>')
def main(article):
    zimply_article_request = requests.get('http://localhost:9454/{}'.format(article))

    soup = BeautifulSoup(zimply_article_request.content)

    for image in soup.find_all(['image', 'img']):
        image.decompose()

    for extra_tags in soup.find_all(['b', 'a', 'span']):
        extra_tags.unwrap()

    title_e = soup.find('h1', { 'class': 'section-heading' }).text.strip()
    body_e = soup.find('div', { 'id': 'mf-section-0' }).text.strip()

    return render_template("wiki.html", title = title_e, content = body_e)

    #return json.dumps({ 'title': title_e.text.strip(), 'body': body_e.text.strip() })
