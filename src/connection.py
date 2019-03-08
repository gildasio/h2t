import requests

def get(url, redirects=True, user_agent="h2t"):
    headers = {'user-agent': user_agent}
    return requests.get(url, allow_redirects=redirects, headers=headers)
