#!/usr/bin/env python3
import argparse
import os

from src import output
from src import banners
from src import connection
from src import files
from src import scan_command
from src import list_command


def show(result, content, category, url='', status=True):
    if len(result) > 0:
        if hasattr(args, "output"):
            output.results(result, content, category, fields=args.print,
                           status=status, output=args.output, url=url)
        else:
            output.results(result, content, category, fields=args.print,
                           status=status)


def check(response, url, category):
    if category == "good":
        content = files.read_json("headers/good.json")
    elif category == "bad":
        content = files.read_json("headers/bad.json")

    result = scan_command.check(response, content, category=category,
                                status=args.status,
                                headers_to_analyze=args.headers)
    result = scan_command.ignore_headers(result, args.ignore_headers)

    show(result, content, category, url, status=args.status)


def list_headers(args):
    bad = files.read_json("headers/bad.json")
    good = files.read_json("headers/good.json")
    result = dict()

    if args.headers:
        result["bad"] = list_command.list_headers(bad, headers=args.headers)
        result["good"] = list_command.list_headers(good, headers=args.headers)
    else:
        result["bad"] = list_command.list_headers(bad)
        result["good"] = list_command.list_headers(good)

    show(result["bad"], bad, "bad")
    show(result["good"], good, "good")


def scan_headers_url(url, args, index=0, urls_qtd=1):
    if "://" not in url:
        url = "http://" + url

    response = connection.get(url, redirects=args.no_redirect,
                              user_agent=args.user_agent,
                              insecure=args.insecure)

    if index == 0:
        output.print_header(url, args.print, args.output)

    if args.verbose:
        output.verbose(response, args.verbose)

    response = {header.lower(): value.lower() for header,
                value in response.headers.items()}

    if args.bad:
        check(response, url, category="bad")
    elif args.good:
        check(response, url, category="good")
    elif args.all:
        check(response, url, category="bad")
        check(response, url, category="good")

    if index + 1 == urls_qtd:
        output.print_footer(args.output)


def scan_headers(args):
    if args.no_explanation:
        output.help()

    if os.path.isfile(args.url):
        urls = files.read_lines(args.url)
        urls_qtd = len(urls)
        for i, url in enumerate(urls):
            scan_headers_url(url, args, index=i, urls_qtd=urls_qtd)
    else:
        scan_headers_url(args.url, args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="h2t - HTTP Hardening Tool")

    sub_parsers = parser.add_subparsers(help="sub-command help")

    list_parser = sub_parsers.add_parser("list", aliases=['l'],
                                         help="show a list of available"
                                              " headers in h2t catalog (that"
                                              " can be used in scan subcommand"
                                              "-H option)")
    list_parser.add_argument("-p", "--print", default=False, nargs="+",
                             help="a list of additional information about the"
                             " headers to print. For now there are two"
                             " options: description and refs (you can use"
                             " either or both)")
    list_parser.add_argument("-B", "--no-banner", action="store_false",
                             default=True, help="don't print the h2t banner")

    group_headers_list = list_parser.add_mutually_exclusive_group()
    group_headers_list.add_argument("-a", "--all", action="store_true",
                                    default=True, help="list all available "
                                    "headers [default]")
    group_headers_list.add_argument("-H", "--headers", nargs="+",
                                    help="a list of headers to look for in"
                                    " the h2t catalog")

    list_parser.set_defaults(command=list_headers)

    scan_parser = sub_parsers.add_parser("scan", aliases=['s'],
                                         help="scan url to hardening headers")
    scan_parser.add_argument("-v", "--verbose", action="count", default=0,
                             help="increase output verbosity: -v print"
                             " response headers, -vv print response and"
                             " request headers")
    scan_parser.add_argument("-a", "--all", action="store_true", default=True,
                             help="scan all cataloged headers [default]")
    scan_parser.add_argument("-g", "--good", action="store_true",
                             help="scan good headers only")
    scan_parser.add_argument("-b", "--bad", action="store_true",
                             help="scan bad headers only")
    scan_parser.add_argument("-H", "--headers", default=False, nargs="+",
                             help="scan only these headers (see available in"
                             " list sub-command)")
    scan_parser.add_argument("-p", "--print", default=False, nargs="+",
                             help="a list of additional information about the"
                             " headers to print. For now there are two"
                             " options: description and refs (you can use"
                             " either or both)")
    scan_parser.add_argument("-i", "--ignore-headers", default=False,
                             nargs="+",
                             help="a list of headers to ignore in the results")
    scan_parser.add_argument("-B", "--no-banner", action="store_false",
                             default=True, help="don't print the h2t banner")
    scan_parser.add_argument("-E", "--no-explanation", action="store_false",
                             default=True,
                             help="don't print the h2t output explanation")
    scan_parser.add_argument("-o", "--output",
                             choices=["normal", "csv", "json"],
                             default="normal",
                             help="choose which output format to use "
                             "(available: normal, csv, json)")

    scan_parser.add_argument("-n", "--no-redirect", action="store_false",
                             help="don't follow http redirects")
    scan_parser.add_argument("-u", "--user-agent",
                             help="set user agent to scan request")
    scan_parser.add_argument("-k", "--insecure", action="store_false",
                             help="don't verify SSL certificate as valid")

    groupOutput = scan_parser.add_mutually_exclusive_group()
    groupOutput.add_argument("-r", "--recommendation", action="store_true",
                             default=True,
                             help="output only recommendations [default]")
    groupOutput.add_argument("-s", "--status", action="store_true",
                             help="output actual status (eg: existent"
                             " headers only)")

    scan_parser.add_argument("url", help="url to look for")
    scan_parser.set_defaults(command=scan_headers)

    args = parser.parse_args()

    if hasattr(args, 'no_banner') and args.no_banner:
        output.banner(banners.get_banner())

    if isinstance(args.headers, list):
        args.headers = {header.lower() for header in args.headers}

    if 'command' in args:
        args.command(args)
    else:
        parser.print_usage()
