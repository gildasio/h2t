from colorama import Fore, Style

def help():
    print('''Output explanation:
    {b}{g}[+]{reset} Good headers. Already used in your website. Good job!
    {b}{y}[+]{reset} Good headers. We recommend apply it
    {b}{r}[-]{reset} Bad headers. We recommend remove it\n'''.format(b=Style.BRIGHT, g=Fore.GREEN, y=Fore.YELLOW, r=Fore.RED, reset=Style.RESET_ALL))

def banner(b):
    print(Style.BRIGHT, end="")
    print(b)
    print("https://github.com/gildasio/h2t")
    print(Style.RESET_ALL)

def printBright(message, end="\n"):
    print(Style.BRIGHT + message + Style.RESET_ALL, end=end)

def printColor(message, color):
    if color == "red":
        color = Fore.RED
    print(color + message + Fore.RESET)

def printLine(message, level=1, category = None, title = None, status=False):
    if category == "good" and status:
        color = Fore.GREEN
        pre = "[+] "
    elif category == "good" and not status:
        color = Fore.YELLOW
        pre = "[+] "
    elif category == "bad":
        color = Fore.RED
        pre = "[-] "
    else:
        color = ''
        pre = ''

    if title:
        print(" "*4*level + Style.BRIGHT + title + ": " + Style.RESET_ALL + message)
    else:
        print(" "*4*level + color + Style.BRIGHT + pre + Fore.RESET + message)

def show(content, fields, category, status=False):
    printLine(content["title"], category=category, status=status)

    if isinstance(fields, list):
        if "description" in fields:
            printLine(content["description"], level=2, title="Description")
        if "refs" in fields:
            printLine('', level=2, title="Refs")
            for item in content["refs"]:
                printLine(Style.RESET_ALL + item, level=3)

    print(Style.RESET_ALL, end="")

def results(result, catalog, category, fields=0, status=False):
    for header in result:
        if header not in catalog:
            printBright(header, end="")
            printColor(" isn't an option. See available option to -H using 'list -a'", "red")
            exit()

        if isinstance(result, dict) and isinstance(result[header], list):
            for i in result[header]:
                show(catalog[header][i], fields, category, status=status)
        elif isinstance(catalog[header], list):
            for item in catalog[header]:
                show(item, fields, category, status=status)
        else:
            show(catalog[header], fields, category, status=status)

def verbose(response, verbose):
    from urllib.parse import urlparse

    req = response.request
    if verbose >= 2:
        printLine(req.method + " " + req.path_url + " HTTP/1.1")
        printLine("Host: " + urlparse(response.url).netloc)
        for header in req.headers:
            printLine(req.headers[header], title=header)
        print()

    if verbose >= 1:
        printLine("HTTP/1.1 " + str(response.status_code) + " " + response.reason)
        for header in response.headers:
            printLine(response.headers[header], title=header)
        print()
