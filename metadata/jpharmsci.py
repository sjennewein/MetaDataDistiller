import json
import requests
from bs4 import BeautifulSoup
from .payload import Payload, Author

def map(url):
    with open('metadata/scheme.json', 'r') as infile:
        meta = Payload(json.load(infile))

    try:
        r = requests.get(url)
    except:
        return {}
    html = BeautifulSoup(r.content, 'html.parser')
    metadata = html.find_all("meta")
    r.close()

    author = False
    for item in metadata:
        if not item.has_attr('name'):
            continue
        if item['name'] == 'citation_publication_date':
            meta.publication_date = item['content']
        elif item['name'] == 'citation_online_date':
            meta.online_date = item['content']
        elif item['name'] == 'citation_author':
            if author:
                meta.authors.append(author)
                author = False
            author = Author(item['content'])
        elif item['name'] == 'citation_author_institution':
            author.affiliations.append(item['content'])
        elif item['name'] == 'citation_issue':
            meta.issues.first= item['content']
        elif item['name'] == 'citation_keywords':
            meta.keywords.append(item['content'])
        elif item['name'] == 'article_references':
            meta.references = item['content']
        elif item['name'] == 'citation_language':
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
    if author:
        meta['authors'].append(author)

    return meta
