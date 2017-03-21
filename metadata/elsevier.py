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
    td = html.find('script', {'type': 'application/json'})

    if td is None:
        return {}

    data = td.contents[0].replace('\\\\', '\\')
    data = data.replace(r'\"', '"')
    obj = json.loads(data[1:-1])

    meta.publication_date = obj['article']['dates']['Publication date']
    if 'Received' in obj['article']['dates']:
        meta.received = obj['article']['dates']['Received']
    meta.online_date = obj['article']['dates']['Available online']

    for name in obj['authors']['authors']:
        member = obj['authors']['authors'][name]

        location = []

        if not member['refs']:
            for loc in obj['authors']['affiliations']:
                location.append(obj['authors']['affiliations'][loc])

        for loc in member['refs']:
            if 'af' in loc.lower():
                location.append(obj['authors']['affiliations'][loc])
            else:
                continue

        if not location:
            for af in obj['authors']['affiliations']:
                location.append(obj['authors']['affiliations'][af])

        meta.authors.append(Author(member['surname'], member['givenName'], location))

    meta.keywords = []
    meta.references = ''
    meta.language = ''
    meta.journal_title = obj['article']['srctitle']
    meta.issn = obj['article']['issn']
    meta.doi = obj['article']['doi']
    meta.title= obj['article']['titlePlain']

    meta.pages.first = obj['article']['pages'][0]['first-page']
    meta.pages.last = obj['article']['pages'][0]['last-page'] if 'last-page' in obj['article']['pages'][0] else ''

    meta.issues.first = obj['article']['iss-first']
    meta.issues.last = obj['article']['iss-last'] if 'iss-last' in obj['article'] else ''
    meta.volumes.first = obj['article']['vol-first']
    meta.volumes.last = obj['article']['vol-last'] if 'vol-last' in obj['article'] else ''
    meta.publisher = obj['article']['imprintPublisher']['displayName']

    return meta
