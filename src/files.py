import json


def read_lines(f):
    with open(f) as content:
        lines = [line.rstrip('\n') for line in content]
        return lines


def read_json(f):
    with open(f) as content:
        data = json.load(content)
        return data
