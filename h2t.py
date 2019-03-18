#!/usr/bin/env python3

import argparse
import os

from src import output
from src import banners
from src import connection
from src import files
from src import scanCommand
from src import listCommand

def show(result, content, category, url='', status=True):
    if len(result) > 0:
        if hasattr(args, "output"):
            output.results(result, content, category, fields=args.print, status=status, output=args.output, url=url)
        else:
            output.results(result, content, category, fields=args.print, status=status)

def check(response, url, category):
    if category == "good":
        content = files.readJSON("headers/good.json")
    elif category == "bad":
        content = files.readJSON("headers/bad.json")

    result = scanCommand.check(response, content, category=category, status=args.status, headers2analyze=args.headers)
    result = scanCommand.ignoreHeaders(result, args.ignore_headers)

    show(result, content, category, url, status=args.status)

def listHeaders(args):
    bad = files.readJSON("headers/bad.json")
    good = files.readJSON("headers/good.json")
    result = dict()

    if args.headers:
        result["bad"] = listCommand.listHeaders(bad, headers=args.headers)
        result["good"] = listCommand.listHeaders(good, headers=args.headers)
    else:
        result["bad"] = listCommand.listHeaders(bad)
        result["good"] = listCommand.listHeaders(good)

    show(result["bad"], bad, "bad")
    show(result["good"], good, "good")

def scanHeadersURL(url, args, index=0, urls_qtd=1):
    if "://" not in url:
        url = "http://" + url

    response = connection.get(url, redirects=args.no_redirect, user_agent=args.user_agent, insecure=args.insecure)

    if index == 0:
        output.printHeader(url, args.print, args.output)

    if args.verbose:
        output.verbose(response, args.verbose)

    response = {header.lower(): value.lower() for header, value in response.headers.items()}

    if args.bad:
        check(response, url, category="bad")
    elif args.good:
        check(response, url, category="good")
    elif args.all:
        check(response, url, category="bad")
        check(response, url, category="good")

    if index + 1 == urls_qtd:
        output.printFooter(args.output)

def scanHeaders(args):
    if args.no_explanation:
        output.help()

    if os.path.isfile(args.url):
        urls = files.readLines(args.url)
        urls_qtd = len(urls)
        for i, url in enumerate(urls):
            scanHeadersURL(url, args, index=i, urls_qtd=urls_qtd)
    else:
        scanHeadersURL(args.url, args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="h2t - HTTP Hardening Tool")

    subParsers = parser.add_subparsers(help="sub-command help")

    listParser = subParsers.add_parser("list", aliases=['l'], help="show a list of available headers in h2t catalog (that can be used in scan subcommand -H option)")
    listParser.add_argument("-p", "--print", default=False, nargs="+", help="a list of additional information about the headers to print. For now there are two options: description and refs (you can use either or both)")
    listParser.add_argument("-B", "--no-banner", action="store_false", default=True, help="don't print the h2t banner")

    groupHeadersList = listParser.add_mutually_exclusive_group()
    groupHeadersList.add_argument("-a", "--all", action="store_true", default=True, help="list all available headers [default]")
    groupHeadersList.add_argument("-H", "--headers", nargs="+", help="a list of headers to look for in the h2t catalog")

    listParser.set_defaults(command=listHeaders)

    scanParser = subParsers.add_parser("scan", aliases=['s'], help="scan url to hardening headers")
    scanParser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity: -v print response headers, -vv print response and request headers")
    scanParser.add_argument("-a", "--all", action="store_true", default=True, help="scan all cataloged headers [default]")
    scanParser.add_argument("-g", "--good", action="store_true", help="scan good headers only")
    scanParser.add_argument("-b", "--bad", action="store_true", help="scan bad headers only")
    scanParser.add_argument("-H", "--headers", default=False, nargs="+", help="scan only these headers (see available in list sub-command)")
    scanParser.add_argument("-p", "--print", default=False, nargs="+", help="a list of additional information about the headers to print. For now there are two options: description and refs (you can use either or both)")
    scanParser.add_argument("-i", "--ignore-headers", default=False, nargs="+", help="a list of headers to ignore in the results")
    scanParser.add_argument("-B", "--no-banner", action="store_false", default=True, help="don't print the h2t banner")
    scanParser.add_argument("-E", "--no-explanation", action="store_false", default=True, help="don't print the h2t output explanation")
    scanParser.add_argument("-o", "--output", choices=["normal", "csv", "json"], default="normal", help="choose which output format to use (available: normal, csv, json)")

    scanParser.add_argument("-n", "--no-redirect", action="store_false", help="don't follow http redirects")
    scanParser.add_argument("-u", "--user-agent", help="set user agent to scan request")
    scanParser.add_argument("-k", "--insecure", action="store_false", help="don't verify SSL certificate as valid")

    groupOutput = scanParser.add_mutually_exclusive_group()
    groupOutput.add_argument("-r", "--recommendation", action="store_true", default=True, help="output only recommendations [default]")
    groupOutput.add_argument("-s", "--status", action="store_true", help="output actual status (eg: existent headers only)")

    scanParser.add_argument("url", help="url to look for")
    scanParser.set_defaults(command=scanHeaders)

    args = parser.parse_args()

    if hasattr(args, 'no_banner') and args.no_banner:
        output.banner(banners.getBanner())

    if isinstance(args.headers, list):
        args.headers = {header.lower() for header in args.headers}

    if 'command' in args:
        args.command(args)
    else:
        parser.print_usage()
