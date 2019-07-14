import json
from urllib.request import urlopen

# Google API reference - https://developers.google.com/books/docs/v1/reference/volumes

def isbn_query(isbn):
    google_api = 'https://www.googleapis.com/books/v1/volumes?q=isbn:%s'
    webdata = urlopen(url = google_api % isbn)
    if not webdata:
        return {}

    webdata = json.loads(webdata.read().decode('utf-8'))
    if not webdata['totalItems']:
        return {}

    # here 'items' is N-th search hit. now only zeroth used
    webdata = webdata['items'][0]['volumeInfo']

    data = {}
    data['authors'] = webdata['authors']
    data['title'] = webdata['title']
    data['subtitle'] = webdata.get('subtitle', '')
    data['publisher'] = webdata.get('publisher', '')
    data['year'] = webdata.get('publisherDate', '').split('-')[0]
    data['pages'] = webdata['pageCount']
    data['language'] = webdata['language']
    data['identifiers'] = {}
    data['identifiers']['isbn'] = [x['identifier'] for x in webdata['industryIdentifiers'] if x['type'] in ['ISBN_10', 'ISBN_13']]

    return data
