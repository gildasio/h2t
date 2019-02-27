from colorama import Fore, Style

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

def show(content, verbose, category, status=False):
	printLine(content["title"], category=category, status=status)

	if verbose >= 1:
		printLine(content["description"], level=2, title="Description")
	if verbose >= 2:
		printLine('', level=2, title="About")
		for item in content["about"]:
			printLine(Style.RESET_ALL + item, level=3)
	if verbose >= 3:
		printLine('', level=2, title="How to")
		for item in content["tech"]:
			printLine(Style.RESET_ALL + item, level=3)


	print(Style.RESET_ALL, end="")

def results(result, catalog, category, verbose=0, status=False):
	for header in result:
		if header not in catalog:
			printBright(header, end="")
			printColor(" isn't an option. See available option to -H using 'list -a'", "red")
			exit()

		if isinstance(result, dict) and isinstance(result[header], list):
			for i in result[header]:
				show(catalog[header][i], verbose, category, status=status)
		elif isinstance(catalog[header], list):
			for item in catalog[header]:
				item["title"] = header + " (" + item["title"] + ")"
				show(item, verbose, category, status=status)
		else:
			show(catalog[header], verbose, category, status=status)
