# h2t - HTTP Hardening Tool

## Description

**h2t** is a simple tool to help sysadmins to hardening their websites.

Until now **h2t** checks the website headers and recommends how to make it better.

## Dependences

* [Python 3](https://www.python.org/download/releases/3.0/)
* [colorama](https://github.com/tartley/colorama)
* [requests](http://docs.python-requests.org/en/master/)

## Install

~~~
$ git clone https://github.com/gildasio/h2t
$ cd h2t
$ pip install -r requirements.txt
$ ./h2t.py -h
~~~

## Usage

**h2t** has subcommands: *list* and *scan*.

~~~
$ ./h2t.py -h
|    /~\ |
|/~\  ./~|~
|   |/__ |

https://github.com/gildasio/h2t

usage: h2t.py [-h] {list,l,scan,s} ...

h2t - HTTP Hardening Tool

positional arguments:
  {list,l,scan,s}  sub-command help
    list (l)       show a list of cataloged headers (allowed for use in -H
                   scan option)
    scan (s)       scan url to hardening headers

optional arguments:
  -h, --help       show this help message and exit
~~~

### List Subcommand

The **list** subcommand lists all headers cataloged in **h2t** and can show informations about it as a description, links for more information and for how to's.

~~~
$ ./h2t.py list -h
     ____ ____ ____
    ||h |||2 |||t ||
    ||__|||__|||__||
    |/__\|/__\|/__\|

https://github.com/gildasio/h2t

usage: h2t.py list [-h] [-v] [-a | -H HEADERS [HEADERS ...]]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -a, --all             List all cataloged headers
  -H HEADERS [HEADERS ...], --headers HEADERS [HEADERS ...]
                        a list of headers to show from catalog
~~~

### Scan Subcommand

The **scan** subcommand perform a scan in a website looking for their headers.

~~~
$ ./h2t.py s -h
|  |_| ||____  | _|  |_
|   _  ||    --||_    _|
|__| |_||______|  |__|
https://github.com/gildasio/h2t

usage: h2t.py scan [-h] [-v] [-a] [-g] [-b] [-H HEADERS [HEADERS ...]]
                   [-i IGNORE_HEADERS [IGNORE_HEADERS ...]] [-n]
                   [-u USER_AGENT] [-r | -s]
                   url

positional arguments:
  url                   url to look for

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -a, --all             look at all cataloged headers
  -g, --good            look at good headers only
  -b, --bad             look at bad headers only
  -H HEADERS [HEADERS ...], --headers HEADERS [HEADERS ...]
                        a list of headers to look for (see available in list
                        sub-command)
  -i IGNORE_HEADERS [IGNORE_HEADERS ...], --ignore-headers IGNORE_HEADERS [IGNORE_HEADERS ...]
                        a list of headers to ignore in the results
  -n, --no-redirect     doesn't follow http redirects
  -u USER_AGENT, --user-agent USER_AGENT
                        set user agent to request
  -r, --recommendation  output only recommendations
  -s, --status          output actual status (eg: existent headers only)
~~~

### Output

For now the output is only in normal mode. Understant it as follows:

* <span style="color: red;">[+]</span> Red Headers are bad headers that open a breach on your website or maybe show a lots of information. We recommend fix it.
* <span style="color: yellow;">[+]</span> Yellow Headers are good headers that is not applied on your website. We recommend apply them.
* <span style="color: green">[-]</span> Green Headers are good headers that is already used in your website. It's shown when use `-s` flag.

Example:

![h2t agains hack.me](docs/hackme.png)

* Cookie HTTP Only would be good to be applied
* Cookie over SSL/TLS would be good to be applied
* Server header would be good to be removed
* Referrer-Policy would be good to be applied
* X-Frame-Options is already in use, nothing to do here
* X-XSS-Protection is already in use, nothing to do here

### Screenshots

#### Help

![h2t help menu](docs/help_main.png)

![h2t help menu for list subcommand](docs/help_list.png)

![h2t help menu for scan subcommand](docs/help_scan.png)

#### My website

![h2t against my website](docs/gildasio.png)

## Contribute

For contribute guidelines look at [CONTRIBUTING](CONTRIBUTING.md)
