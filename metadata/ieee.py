import json
import requests
from bs4 import BeautifulSoup
from .payload import Payload, Author


def map(url):
    meta = Payload()

    try:
        r = requests.get(url)
    except:
        return {}
    html = BeautifulSoup(r.content, 'html.parser')
    r.close()
    td = html.find_all('script', {'type': 'text/javascript'})

    data = ''
    for element in td:
        if len(element.contents) == 0:
            continue
        if 'global.document.metadata' in element.contents[0]:
            matching = [s for s in element.contents[0].split('\n') if "global.document.metadata" in s]
            data = '='.join(matching[0].split('=')[1:])

    obj = json.loads(data[:-1])

    meta.publication_date = obj['journalDisplayDateOfPublication']
    meta.received = ''
    meta.online_date = obj['onlineDate']

    if obj['sections']['authors'] == 'true' and 'authors' in obj:
        for member in obj['authors']:
            author = Author(member['name'])
            author.affiliations.append(member['affiliation'])
            meta.authors.append(author)

    if obj['sections']['keywords'] == 'true' and 'keywords' in obj:
        for keyword in obj['keywords'][0]['kwd']:
            meta.keywords.append(keyword)
    meta.references = ''
    meta.language = ''
    meta.journal_title = obj['publicationTitle']
    meta.issn = obj['issn'][0]['value']
    meta.doi = obj['doi']
    meta.title = obj['title']

    meta.pages.first = obj['startPage']
    meta.pages.last = obj['endPage']

    meta.issues.first = obj['issue']
    meta.volumes.first = obj['volume']
    meta.publisher = obj['publisher']

    return meta
