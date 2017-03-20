import json
import requests
from bs4 import BeautifulSoup
from .payload import Payload


def map(url):
    meta = Payload()

    try:
        r = requests.get(url)
    except:
        return {}
    html = BeautifulSoup(r.content, 'html.parser')
    metadata = html.find_all("meta")
    r.close()

    author = {}
    for item in metadata:
        if not item.has_attr('name'):
            continue
        if item['name'] == 'dc.Date':
            meta['publication_date'] = item['content']
        elif item['name'] == '':
            meta['online_data'] = ''
        elif item['name'] == 'dc.Creator':
            author['name'] = item['content']
            meta['authors'].append(author)
        elif item['name'] == '':
            meta['issue'] = '' 
        elif item['name'] == 'keywords':
            meta['keywords'].append([key.strip() for key in item['content'].split(',')])
        elif item['name'] == '':
            meta['references'] = '' 
        elif item['name'] == 'dc.Language':
            meta['language'] = item['content']
        elif item['name'] == 'dc.Title':
            meta['journal_title'] = item['content']
        elif item['name'] == '':
            meta['issn'] = ''
        elif item['name'] == 'dc.Identifier':
            meta['doi'] = item['content']
        elif item['name'] == 'dc.Title':
            meta['title'] = item['content']
        elif item['name'] == '':
            meta['first_page'] = ''
        elif item['name'] == '':
            meta['last_page'] = ''
        elif item['name'] == '':
            meta['volume'] = '' 
        elif item['name'] == 'dc.Publisher':
            meta['publisher'] = item['content']

    return meta
