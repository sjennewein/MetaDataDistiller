import json
import requests
from bs4 import BeautifulSoup
from .payload import Payload, Author, Affiliation
from metadata import nmd
from metadata import bioaging
import re


def map(url):
    meta = Payload()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
        'From': 'youremail@domain.com'
    }

    try:
        r = requests.get(url, headers=headers)
    except:
        return {}
    html = BeautifulSoup(r.content, 'html.parser')
    r.close()

    if 'nmd-journal' in r.url:
        return nmd.map(url)
    elif 'neurobiologyofaging' in r.url:
        return bioaging.map(url)

    td = html.find('script', {'type': 'application/json'})

    if td is None:
        return map2(html)

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
    meta.title = obj['article']['titlePlain']

    meta.pages.first = obj['article']['pages'][0]['first-page']
    meta.pages.last = obj['article']['pages'][0]['last-page'] if 'last-page' in obj['article']['pages'][0] else ''

    meta.issues.first = obj['article']['iss-first'] if 'iss-first' in obj['article'] else ''
    meta.issues.last = obj['article']['iss-last'] if 'iss-last' in obj['article'] else ''
    meta.volumes.first = obj['article']['vol-first']
    meta.volumes.last = obj['article']['vol-last'] if 'vol-last' in obj['article'] else ''
    meta.publisher = obj['article']['imprintPublisher']['displayName']

    return meta


def map2(html):
    meta = Payload()
    td = html.find('title')
    if td:
        data = td.contents[0]
        meta.title = str(data).strip()

    td = html.find('ul', {'class': 'authorGroup'})
    authors = {}
    affiliation = {}
    if td:
        for li in td.children:
            reference = []
            name = str(li.find_all('a')[0].contents[0])
            if li.find('sup'):
                for sup in li.find_all('sup'):
                    if sup.contents[0].isalpha():
                        reference.append(str(sup.contents[0]))
            else:
                reference.append('a')
            authors[name] = reference

    td = html.find('ul', {'class': 'affiliation'})
    if td:
        for li in td.children:
            if li.find('sup'):
                reference = str(li.find('sup').contents[0])
            else:
                reference = 'a'
            institute = str(li.find('span').contents[0])
            affiliation[reference] = institute

    for author in authors:
        writer = Author(author)
        for ref in authors[author]:
            writer.affiliations.append(Affiliation(affiliation[ref]))
        meta.authors.append(writer)

    td = html.find('p', {'class': 'volIssue'})
    for token in td.text.split(','):
        if 'volume' in token.lower():
            m = re.search('([0-9]+).([0-9]+)', token)
            if not m:
                m = re.search('([0-9]+)', token)
                meta.volumes.first = str(m.group(1))
                continue

            meta.volumes.first = m.group(0)
            meta.volumes.last = m.group(1)
        elif 'issue' in token.lower():
            m = re.search('([0-9]+).([0-9]+)', token)
            if not m:
                m = re.search('([0-9]+)', token)
                meta.issues.first = m.group(1)
                continue

            meta.issues.first = m.group(1)
            meta.issues.last = m.group(2)
        elif 'page' in token.lower():
            m = re.search('([0-9]+).([0-9]+)', token)
            if not m:
                m = re.search('([0-9]+)', token)
                meta.pages.first = m.group(1)
                continue

            meta.pages.first = m.group(1)
            meta.pages.last = m.group(2)

    td = html.find('div', {'class': 'title'})
    meta.journal_title = str(td.find('span').contents[0])
    meta.publisher = 'Elsevier'
    td = html.find('dl', {'class': 'articleDates'})
    data = td.find('dd').contents[0].split(',')
    accepted = ''
    online = ''
    received = ''
    for dates in data:
        if 'accepted' in dates.lower():
            m = re.search('([0-9]+.*[0-9]+)', dates)
            accepted = str(m.group(0))
        elif 'available' in dates.lower():
            m = re.search('([0-9]+.*[0-9]+)', dates)
            online = str(m.group(0))
        elif 'received' in dates.lower():
            m = re.search('([0-9]+.*[0-9]+)', dates)
            received = str(m.group(0))
    meta.online_date = online
    meta.publication_date = accepted
    meta.received = received
    td = html.find_all('script')
    doi = False
    for script in td:
        for element in script.contents:
            if 'doi' in element:
                for item in element.split(';'):
                    if 'SDM.doi' in item:
                        m = re.search("'(.*)'", item)
                        data = m.groups()
                        meta.doi = str(data[0])
                        doi = True
                        break
            if doi:
                break
        if doi:
            break

    td = html.find('ul', {'class': 'keyword'})
    if td:
        for keyword in td.text.split(';'):
            meta.keywords.append(keyword.strip())

    return meta
