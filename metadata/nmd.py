import json
import requests
from bs4 import BeautifulSoup
from .payload import Payload, Author, Affiliation


def map(url):
    meta = Payload()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
        'From': 'youremail@domain.com'
    }
    session = requests.Session()
    try:
        r = session.get(url, headers=headers)
    except:
        return {}
    html = BeautifulSoup(r.content, 'html.parser')
    print(html)
    td = html.find_all('iframe')
    iframes = []
    for item in td:
        iframes.append(session.get('http:' + item.get('src')))
    r.close()
    td = html.find('a')
    url = td.get('href')

    try:
        r = session.get(url, headers=headers)
    except:
        return {}

    html = BeautifulSoup(r.content, 'html.parser')
    session.close()

    metadata = html.find_all("meta")
    r.close()

    author = None
    for item in metadata:
        if not item.has_attr('name'):
            continue
        if item['name'] == 'citation_publication_date':
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
        meta.authors.append(author)

    return meta
