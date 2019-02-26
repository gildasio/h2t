from colorama import Fore, Style

def banner(b):
    print(Style.BRIGHT, end="")
    print(b)
    print("https://github.com/gildasio/h2t")
    print(Style.RESET_ALL)

def printLine(message, level=0, category = None, title = None):
	if category == "good":
		color = Fore.GREEN
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

def show(content, verbose, category):
	printLine(content["title"], category=category)

	if verbose >= 1:
		printLine(content["description"], level=1, title="Description")
	if verbose >= 2:
		printLine('', level=1, title="About")
		for item in content["about"]:
			printLine(Style.RESET_ALL + item, level=2)
	if verbose >= 3:
		printLine('', level=1, title="How to")
		for item in content["tech"]:
			printLine(Style.RESET_ALL + item, level=2)


	print(Style.RESET_ALL, end="")

def results(result, catalog, category, verbose=0):
	for header in result:
		if isinstance(result, dict) and isinstance(result[header], list):
			for i in result[header]:
				show(catalog[header][i], verbose, category)
		else:
			show(catalog[header], verbose, category)
