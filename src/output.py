import json
from urllib.parse import urlparse
from colorama import init, Fore, Style

init()


def help():
    print('''Output explanation:
    {b}{g}[+]{reset} Good headers. Already used in your website. Good job!
    {b}{y}[+]{reset} Good headers. We recommend applying it
    {b}{r}[-]{reset} Bad headers. We recommend remove it\n'''.format(b=Style.BRIGHT, g=Fore.GREEN, y=Fore.YELLOW, r=Fore.RED, reset=Style.RESET_ALL))


def banner(b):
    print(Style.BRIGHT, end='')
    print(b)
    print('https://github.com/gildasio/h2t')
    print(Style.RESET_ALL)


def print_bright(message, end='\n'):
    print(Style.BRIGHT + message + Style.RESET_ALL, end=end)


def print_color(message, color):
    if color == 'red':
        color = Fore.RED
    print(color + message + Fore.RESET)


def get_status(category, status):
    if category == 'good' and status:
        return 'applied'
    elif category == 'good' and not status:
        return 'touse'
    elif category == 'bad':
        return 'toremove'


def print_line(message, level=1, category = None, title = None, status=False):
    sts = get_status(category, status)

    if sts == 'applied':
        color = Fore.GREEN
        pre = '[+] '
    elif sts == 'touse':
        color = Fore.YELLOW
        pre = '[+] '
    elif sts == 'toremove':
        color = Fore.RED
        pre = '[-] '
    else:
        color = ''
        pre = ''

    if title:
        print(' '*4*level + Style.BRIGHT + title + ': ' + Style.RESET_ALL + message)
    else:
        print(' '*4*level + color + Style.BRIGHT + pre + Fore.RESET + message)


def print_header(url, fields, output):
    if output == 'normal':
        print_bright(url)
    elif output == 'csv':
        csv_header(fields)
    elif output =='json':
        print('[\n\t{\'url\': '' + url + '',')
        print('\t\'headers\': [')


def print_footer(output):
    if output == 'json':
        print('\t]}\n]')


def csv_header(fields, delimiter=';'):
    print('url' + delimiter + 'status' + delimiter + 'title', end='')

    if isinstance(fields, list):
        for field in fields:
            print(delimiter + field, end='')

    print()


def show(content, fields, category, status=False, output='normal', url=''):
    if output == 'normal':
        show_normal(content, fields, category, status)
    elif output == 'csv':
        show_csv(content, fields, category, status, url)
    elif output == 'json':
        show_json(content, fields, category, status)


def show_json(content, fields, category, status):
    sts = get_status(category, status)

    result = {
        'title': content['title'],
        'status': sts
    }

    if isinstance(fields, list):
        if 'description' in fields:
            result['description'] = content['description']
        if 'refs' in fields:
            result['refs'] = content['refs']

    print('\t\t' + json.dumps(result) + ',')


def show_csv(content, fields, category, status, url, delimiter=';'):
    sts = get_status(category, status)

    if sts == 'applied':
        status = 'applied'
    elif sts == 'touse':
        status = 'recommended to use'
    elif sts == 'toremove':
        status = 'recommended to remove'

    print(url, end=delimiter)
    print(status, end=delimiter)
    print(content['title'], end='')

    if isinstance(fields, list):
        if 'description' in fields:
            print(delimiter + content['description'], end='')
        if 'refs' in fields:
            print(delimiter, end='')
            for item in content['refs']:
                print(item + ' ', end='')
    print()


def show_normal(content, fields, category, status):
    print_line(content['title'], category=category, status=status)

    if isinstance(fields, list):
        if 'description' in fields:
            print_line(content['description'], level=2, title='Description')
        if 'refs' in fields:
            print_line('', level=2, title='Refs')
            for item in content['refs']:
                print_line(Style.RESET_ALL + item, level=3)
    print(Style.RESET_ALL, end='')


def results(result, catalog, category, fields=0, status=False, output='normal', url=''):
    for header in result:
        if header not in catalog:
            print_bright(header, end='')
            print_color(" isn't an option. See available option to -H using 'list -a'", 'red')
            exit()

        if isinstance(result, dict) and isinstance(result[header], list):
            for i in result[header]:
                show(catalog[header][i], fields, category, status=status, output=output, url=url)
        elif isinstance(catalog[header], list):
            for item in catalog[header]:
                show(item, fields, category, status=status, output=output)
        else:
            show(catalog[header], fields, category, status=status, output=output, url=url)


def verbose(response, verbose):
    req = response.request
    if verbose >= 2:
        print_line(req.method + ' ' + req.path_url + ' HTTP/1.1')
        print_line('Host: ' + urlparse(response.url).netloc)
        for header in req.headers:
            print_line(req.headers[header], title=header)
        print()

    if verbose >= 1:
        print_line('HTTP/1.1 ' + str(response.status_code) + ' ' + response.reason)
        for header in response.headers:
            print_line(response.headers[header], title=header)
        print()
