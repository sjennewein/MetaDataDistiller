import requests
from bs4 import BeautifulSoup
from .payload import Payload,Author


def map(url):
    meta = Payload()

    try:
        r = requests.get(url)
    except:
        return {}
    html = BeautifulSoup(r.content, 'html.parser')
    metadata = html.find_all("meta")
    r.close()


    for item in metadata:
        if not item.has_attr('name'):
            continue
        if item['name'] == 'citation_year':
            meta.publication_date = item['content']
        elif item['name'] == 'citation_online_date':
            meta.online_date = item['content']
        elif item['name'] == 'citation_authors':
            for author in item['content'].split(';'):
                meta.authors.append(Author(author))
        elif item['name'] == 'citation_issue':
            meta.issues.first= item['content']
        elif item['name'] == 'dc.language':
            meta.language = item['content']
        elif item['name'] == 'citation_journal_title':
            meta.journal_title = item['content']
        elif item['name'] == 'citation_issn':
            meta.issn = item['content']
        elif item['name'] == 'citation_doi':
            meta.doi = item['content']
        elif item['name'] == 'citation_title':
            meta.title = item['content']
        elif item['name'] == 'citation_firstpage':
            meta.pages.first = item['content']
        elif item['name'] == 'citation_lastpage':
            meta.pages.last = item['content']
        elif item['name'] == 'citation_volume':
            meta.volumes.first = item['content']
        elif item['name'] == 'citation_publisher':
            meta.publisher = item['content']

    return meta
