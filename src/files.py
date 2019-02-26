import json

def read(f):
    with open(f) as content:
        data = json.load(content)
        return data
