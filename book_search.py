import os
import json

def search(keyword):
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
                text =  data['text']
                if keyword in text:
                    index = text.find(keyword)

                    possible_files[filename] = text[index:index + 20] + "..."
        else:
            continue
    return possible_files