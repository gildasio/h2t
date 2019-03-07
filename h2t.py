#!/usr/bin/env python3

import argparse
import os

from src import output
from src import banners
from src import connection
from src import files
from src import scanCommand
from src import listCommand

def show(result, content, category, status=True):
	if len(result) > 0:
		output.results(result, content, category, verbose=args.verbose, status=status)

def check(response, category):
	if category == "good":
		content = files.readJSON("headers/good.json")
	elif category == "bad":
		content = files.readJSON("headers/bad.json")

	result = scanCommand.check(response, content, category=category, status=args.status, headers2analyze=args.headers)
	result = scanCommand.ignoreHeaders(result, args.ignore_headers)

	show(result, content, category, status=args.status)

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

def scanHeadersURL(url, args):
	if "://" not in url:
		url = "http://" + url

	response = connection.get(url, redirects=args.no_redirect, user_agent=args.user_agent)

	output.printBright(url)

	if args.bad:
		check(response, category="bad")
	elif args.good:
		check(response, category="good")
	elif args.all:
		check(response, category="bad")
		check(response, category="good")

def scanHeaders(args):
	output.help()

	if os.path.isfile(args.url):
		urls = files.readLines(args.url)
		for url in urls:
			scanHeadersURL(url, args)
	else:
		scanHeadersURL(args.url, args)

if __name__ == '__main__':
	output.banner(banners.getBanner())

	parser = argparse.ArgumentParser(description="h2t - HTTP Hardening Tool")

	subParsers = parser.add_subparsers(help="sub-command help")
	
	listParser = subParsers.add_parser("list", aliases=['l'], help="show a list of cataloged headers (allowed for use in -H scan option)")
	listParser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity")

	groupHeadersList = listParser.add_mutually_exclusive_group()
	groupHeadersList.add_argument("-a", "--all", action="store_true", default=True, help="List all cataloged headers")
	groupHeadersList.add_argument("-H", "--headers", nargs="+", help="a list of headers to show from catalog")

	listParser.set_defaults(command=listHeaders)

	scanParser = subParsers.add_parser("scan", aliases=['s'], help="scan url to hardening headers")
	scanParser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity")
	scanParser.add_argument("-a", "--all", action="store_true", default=True, help="look at all cataloged headers")
	scanParser.add_argument("-g", "--good", action="store_true", help="look at good headers only")
	scanParser.add_argument("-b", "--bad", action="store_true", help="look at bad headers only")
	scanParser.add_argument("-H", "--headers", default=False, nargs="+", help="a list of headers to look for (see available in list sub-command)")
	scanParser.add_argument("-i", "--ignore-headers", default=False, nargs="+", help="a list of headers to ignore in the results")

	scanParser.add_argument("-n", "--no-redirect", action="store_false", help="doesn't follow http redirects")
	scanParser.add_argument("-u", "--user-agent", default=False, help="set user agent to request")

	groupOutput = scanParser.add_mutually_exclusive_group()
	groupOutput.add_argument("-r", "--recommendation", action="store_true", default=True, help="output only recommendations")
	groupOutput.add_argument("-s", "--status", action="store_true", help="output actual status (eg: existent headers only)")

	scanParser.add_argument("url", help="url to look for")
	scanParser.set_defaults(command=scanHeaders)

	args = parser.parse_args()

	if 'command' in args:
		args.command(args)
	else:
		parser.print_usage()
