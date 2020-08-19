#from __future__ import print_function, absolute_import, division
import sys
import os
import requests
import re
import time


def usage(argv=sys.argv):
    print(
        "Usage: {} <url> <path to dictionary> \n"
        "Ex: python http://example.com "
        "/tmp/dictionary/wordlist.txt".format(argv[0])
    )


_EXT = (
    ".html",
    ".htm",
    ".php",
    ".css",
    ".js",
    ".txt",
    ".jpg",
    ".png",
    ".sql",
    ".jsp",
    ".asp",
    ".aspx",
)


def _process(line, full_url):
    url = "{}/{}".format(full_url, line.strip())
    r = requests.head(url)
    if r.status_code == 200 or r.status_code == 301:
        print("{} | CODE: {}".format(url, r.status_code))
#    else:
#        print("{} |  CODE: {}".format(url, r.status_code))
#        time.sleep(2.0)
    for extension in _EXT:
        saved_url = "{}{}".format(url, extension)
        r = requests.head(saved_url)
        if r.status_code == 200 or r.status_code == 301:
            print("{} | CODE: {}".format(saved_url, r.status_code))
            time.sleep(2.0)


def main():
    if len(sys.argv) != 3:
        usage()
        return 1

    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    dictionaryPath = sys.argv[2]
    full_url = sys.argv[1]

    if not re.match(regex, full_url):
        print("Invalid url")
        return 1
    if not os.path.isfile(dictionaryPath):
        print("{} doesn't exist".format(dictionaryPath))
        return 1
    try:
        with open(dictionaryPath, "r") as dictionary:
            for line in dictionary:
                _process(line=line, full_url=full_url)

    except requests.ConnectionError:
        return "Failed to connect..."




if __name__ == "__main__":
    sys.exit(main())
