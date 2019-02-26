import requests

def get(url, ret="headers", redirects=True):
    r = requests.get(url, allow_redirects=redirects)
    if ret == "headers":
        return r.headers
