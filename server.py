import requests
import os
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

@app.route('/book_search')
def search_books():
    keyword = request.args.get('q')
    if not os.path.isdir("books"):
        print("No books directory found. Exiting...")
        return
    directory = os.fsencode("books")
    possible_files = {}
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            with open("books/" + filename) as json_file:
                data = json.load(json_file)
                text = data['text']
                if keyword in text:
                    index = text.find(keyword)

                    possible_files[filename] = text[index:index + 20] + "..."
        else:
            continue

    return json.dumps(possible_files)

@app.route('/book/<book>')
def book_get():
    id = request.args.get('q')
    text = ""
    if not os.path.isdir("books"):
        print("No books directory found. Exiting...")
        return
    with open("books/" + str(id) + '.json', 'r') as file:
        text = file.read()

    return text

@app.route('/<article>')
def main(article):
    zimply_article_request = requests.get('http://localhost:9454/{}'.format(article))
    return zimply_article_request.content

    #return json.dumps({ 'title': title_e.text.strip(), 'body': body_e.text.strip() })
