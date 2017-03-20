import json
import requests
from bs4 import BeautifulSoup
from .payload import Payload, Author, Affiliation


def map(url):
    meta = Payload()

    try:
        r = requests.get(url)
    except:
        return {}
    html = BeautifulSoup(r.content, 'html.parser')
    metadata = html.find_all("meta")
    r.close()

    author = None
    for item in metadata:
        if not item.has_attr('name'):
            continue
        if item['name'] == 'prism.publicationDate':
            meta.publication_date = item['content']
        elif item['name'] == 'citation_online_date':
            meta.online_date = item['content']
        elif item['name'] == 'citation_author':
            author = Author(item['content'])
            meta.authors.append(author)
        elif item['name'] == 'citation_author_institution':
            author.affiliations.append(Affiliation(item['content']))
        elif item['name'] == 'citation_issue':
            meta.issues.first = item['content']
        elif item['name'] == 'citation_keywords':
            meta.keywords.append(item['content'])
        elif item['name'] == 'article_references':
            meta.references = item['content']
        elif item['name'] == 'dc.language':
            meta.language = item['content']
        elif item['name'] == 'citation_journal_title':
            meta.journal_title = item['content']
        elif item['name'] == 'prism.issn':
            meta.issn = item['content']
        elif item['name'] == 'citation_doi':
            meta.doi = item['content']
        elif item['name'] == 'citation_title':
            meta.title = item['content']
        elif item['name'] == 'prism.startingPage':
            meta.pages.first = item['content']
        elif item['name'] == 'prism.endingPage':
            meta.pages.last = item['content']
        elif item['name'] == 'prism.volume':
            meta.volumes.first = item['content']
        elif item['name'] == 'citation_publisher':
            meta.publisher = item['content']
    if author:
        meta.authors.append(author)

    return meta
