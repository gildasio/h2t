import json

def readLines(f):
    with open(f) as content:
        lines = [line.rstrip('\n') for line in content]
        return lines

def readJSON(f):
    with open(f) as content:
        data = json.load(content)
        return data
