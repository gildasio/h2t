import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def get(url, redirects=True, user_agent='h2t', insecure=True):
    if not insecure:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    headers = {'user-agent': user_agent}
    return requests.get(url, allow_redirects=redirects, headers=headers, verify=insecure)
