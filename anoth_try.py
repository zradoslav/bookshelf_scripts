import os, sys, shlex, subprocess
import json
from urllib.request import urlopen


def confirm(prompt = "Continue"):
    answer = ""
    question = "{} [yn]? ".format(prompt)
    while answer not in ["y", "n"]:
        answer = input(question).lower()
    return answer == "y"


def choice(variants, prompt):
    enum = range(len(variants))
    for i in enum:
        print(i, variants[i])

    answer = None
    question = "{}: ".format(prompt)
    while answer not in enum:
        answer = int(input(question))
    return variants[answer]


def google_data(isbn):
    webdata = urlopen(url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:%s' % isbn, timeout = 1000)
    if not webdata:
        return {}

    data = {}
    webdata = json.loads(webdata.read().decode('utf-8'))
    if not webdata["totalItems"]:
        return data

    # here 'items' is N-th search hit. now only zeroth used
    webdata = webdata["items"][0]["volumeInfo"]

    data['authors'] = webdata['authors']
    data['title'] = webdata['title']
    data['subtitle'] = webdata.get('subtitle', '')
    data['publisher'] = webdata.get('publisher', '')
    data['year'] = webdata.get('publisherDate', '').split('-')[0]

    return data


def construct_str(data):
    str = '{} - {}'.format(', '.join(data["authors"]), data["title"])

    if data["subtitle"]:
        str = str + ': {}'.format(data["subtitle"])

    if data["publisher"] and data["year"]:
        str = str + " [{}, {}]".format(data["publisher"], data["year"])
    else:
        str = str + " [{}]".format([elem for elem in [data["publisher"], data["year"], "none"] if elem][0])

    return str


def routines(filename, isbn):
    isbn = "".join(isbn.split('-'))
    data    = google_data(isbn)
    if not data:
        print('FAIL: Google Books fetch failed')
        exit(-1)
    else:
        print("OK: Google Books fetch succeeded")

    extension = filename.split('.')[-1].lower()
    end_str = construct_str(data) + ".{}".format(extension)

    print("Rename:\n'%s'\n-->>\n'%s'" % (filename, end_str))
    if confirm():
        os.makedirs('done', exist_ok = True)
        os.rename(filename, 'done/'+ end_str)


def main(filename, n = 4):
    extension = filename.split('.')[-1].lower()
    cmd_str = "isbn_extract -t %s -n %s -f '%s'" % (extension, n, filename)
    cmd_arg = shlex.split(cmd_str)
    output  = subprocess.check_output(cmd_arg).decode("utf-8").splitlines()
    if not output:
        print('FAIL: cannot determine ISBN')
        exit(-1)
    else:
        print('OK: determined ISBN:', output)

    isbn = output
    if len(isbn) > 1:
        isbn = choice(isbn, "Which ISBN?")
    else:
        isbn = isbn[0]

    routines(filename, isbn)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.exit('Wrong argument number')
