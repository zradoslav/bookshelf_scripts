import json
from urllib.request import urlopen

# Open Library API reference -  ttps://openlibrary.org/dev/docs/api/books

def isbn_query(isbn):
    openlibrary_api = 'http://openlibrary.org/api/books?jscmd=data&format=json&bibkeys=%s'
    webdata = urlopen(url = openlibrary_api % isbn)
    if not webdata:
        return {}

    webdata = json.loads(webdata.read().decode('utf-8'))
    if not webdata:
        return {}

    # access to specific hit
    webdata = webdata[isbn] or webdata["ISBN:%s" % isbn]

    data = {}
    data['authors'] = [x['name'] for x in webdata['authors']]
    data['title'] = webdata['title']
    data['subtitle'] = ''
    data['publisher'] = [x['name'] for x in webdata['publishers']][0] # temp w/a
    data['year'] = webdata['publish_date']
    data['pages'] = webdata['number_of_pages']
    #data['language'] = webdata['language']

    data['identifiers'] = {}
    data['identifiers']['isbn'] = webdata['identifiers'].get('isbn_10', []) + webdata['identifiers'].get('isbn_13', [])
    data['identifiers']['lccn'] = webdata['identifiers'].get('lccn', "")
    data['identifiers']['oclc'] = webdata['identifiers'].get('oclc', []) # may be several

    data['classifications'] = {}
    data['classifications']['ddc'] = webdata['classifications']['dewey_decimal_class']
    data['classifications']['lcc'] = webdata['classifications']['lc_classifications']

    return data

