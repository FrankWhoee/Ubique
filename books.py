from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

import json

for i in range(0,100000):
    try:
        text = strip_headers(load_etext(i)).strip()
        book = {}
        book["text"] = text;
        book_json = json.dumps(book)
        with open("books/" + str(i) + '.json', 'w', encoding='utf-8') as outfile:
            print(book_json, file=outfile)
        print("Saved " + str(i) + " to books/" + str(i) + ".json")
    except:
        print(str(i) + " does not exist.")