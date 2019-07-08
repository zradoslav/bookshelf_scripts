import sys, json
import re
from urllib.request import urlopen

# find book metadata by md5 hash

def libgen_query(md5hash, fields):
    fields = ','.join(fields)

    # mirror = http://gen.lib.rus.ec/json.php
    data = urlopen(url = 'http://libgen.io/json.php?md5=%s&fields=%s' % (md5hash, fields),
                   timeout = 1000)
    data = json.loads(data.read().decode('utf-8'))
    data = data[0]

    data['author'] = re.split('\s*,\s*', data['author'])
    data['isbn'] = data['isbn'].replace('-', '').split(',')

    return data # returns Python dict


# libgen API fields - http://libgen.io/json.php

# id, title, volumeinfo, series, periodical, author, year, edition, publisher, city,
# pages, pagesInFile, language, topic, library, library_issue,
# isbn, issn, asin, udc, lbc, ddc, lcc, doi, googlebookid, openlibraryid,
# commentary, dpi, color, cleaned, orientation, paginated, scanned, bookmarked,
# searchable, filesize, extension, md5, generic, visible, locator, local,
# timeadded, timelastmodified, coverurl, tags, identifierwodash,
# descr, toc, crc32, edonkey, aich, sha1, tth, torrent, btih, sha256

def main():
    if len(sys.argv) is not 1:
        all_fields = ['author', 'city', 'edition', 'language', 'pages', 'periodical',
                      'publisher', 'series', 'title', 'volumeinfo', 'year', 'asin',
                      'ddc', 'doi', 'googlebookid', 'isbn', 'issn', 'lbc',
                      'lcc', 'openlibraryid', 'udc']

        data = libgen_query(sys.argv[1], all_fields)
        print(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
    else:
        sys.exit('Wrong arguments number')


if __name__ == '__main__':
    main()
