#!/usr/bin/env python3

import argparse

from src import output
from src import banners
from src import connection
from src import files
from src import core

def check(response, category):
	if category == "good":
		content = files.read("headers/good.json")
	elif category == "bad":
		content = files.read("headers/bad.json")

	result = core.check(response, content, category=category, status_only=args.status)
	if len(result) > 0:
		output.results(result, content, category, verbose=args.verbose)

if __name__ == '__main__':
	output.banner(banners.getBanner())

	parser = argparse.ArgumentParser(description="h2t - HTTP Hardening Tool")
	parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity")
	parser.add_argument("-a", "--all", action="store_true", default=True, help="look at all cataloged headers")
	parser.add_argument("-g", "--good", action="store_true", help="look at good headers only")
	parser.add_argument("-b", "--bad", action="store_true", help="look at bad headers only")
	parser.add_argument("-n", "--no-redirect", action="store_false", help="doesn't follow http redirects")

	groupOutput = parser.add_mutually_exclusive_group()
	groupOutput.add_argument("-r", "--recommendation", action="store_true", default=True, help="output only recommendations")
	groupOutput.add_argument("-s", "--status", action="store_true", help="output recommendations and actual status (eg: existent headers)")

	parser.add_argument("url", help="url to look for")

	args = parser.parse_args()

	if "://" not in args.url:
		args.url = "http://" + args.url

	response = connection.get(args.url, redirects=args.no_redirect)

	if args.all:
		check(response, category="bad")
		check(response, category="good")
	elif args.bad:
		check(response, category="good")
	elif args.good:
		check(response, category="good")
