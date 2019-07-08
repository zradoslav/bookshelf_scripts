import sys, json
from urllib.request import urlopen


def openlibrary_query(isbn):
    query = 'ISBN:%s'
    if isinstance(isbn, list):
        query = query % ',ISBN:'.join(isbn)
    else:
        query = query % isbn

    openlibrary_api = 'http://openlibrary.org/api/books?jscmd=data&format=json&bibkeys=%s'
    data = urlopen(url = openlibrary_api % query, timeout = 1000)
    data = json.loads(data.read().decode('utf-8'))

    return data # returns Python dict


def main():
    if len(sys.argv) is not 1:
        data = openlibrary_query(sys.argv[1])
        print(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
    else:
        sys.exit('Wrong arguments number')


if __name__ == '__main__':
    main()
