import requests
import os
import json

from bs4 import BeautifulSoup

from flask import Flask, request, render_template, send_from_directory
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("wiki_search.html")

@app.route("/book_searcher")
def yeet():
    return render_template("book_searcher.html")

@app.route('/assets/<path>')
def send_assets(path):
    return send_from_directory('assets', path)

@app.route('/search_wikipedia')
def search_wikipedia():
    query = request.args.get('q')
    error = ""

    zimply_request = requests.get('http://localhost:9454/?q={}'.format(query))
    soup = BeautifulSoup(zimply_request.content)

    links = {}

    counter = 0
    for link in soup.findAll('a'):
        if counter > 30:
            break

        href = link.get('href')

        links[link.text] = "/{}".format(href)
        counter += 1

    if counter == 0:
        error = "No results found."
    # return json.dumps(links)
    return render_template("wiki_results.html", links=links.items(), error=error)

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
                    possible_files[text[index:index + 20] + "..."] = filename[0:filename.find(".json")]
        else:
            continue
    print(possible_files)
    return render_template("book_results.html", links=possible_files.items())

@app.route('/book/<book>')
def book_get(book):
    text = ""
    if not os.path.isdir("books"):
        print("No books directory found. Exiting...")
        return
    with open("books/" + str(book) + '.json', 'r') as file:
        text = file.read()
    data = json.loads(text)
    return render_template("book.html", text=data["text"])

@app.route("/<article>")
def article(article):
    return render_template("wiki.html", article_name=article)

@app.route('/embed/<article>')
def main(article):
    zimply_article_request = requests.get('http://localhost:9454/{}'.format(article))

    soup = BeautifulSoup(zimply_article_request.content)

    for image in soup.find_all(['img', 'image']):
        image.decompose()

    return str(soup)

    #return json.dumps({ 'title': title_e.text.strip(), 'body': body_e.text.strip() })
