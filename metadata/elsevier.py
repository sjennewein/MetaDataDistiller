import json
import requests
from bs4 import BeautifulSoup
from .payload import Payload, Author
import re


def map(url):
    meta = Payload()

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'From': 'youremail@domain.com'
    }

    try:
        r = requests.get(url, headers=headers)
    except:
        return {}
    html = BeautifulSoup(r.content, 'html.parser')
    r.close()
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

    meta.issues.first = obj['article']['iss-first']
    meta.issues.last = obj['article']['iss-last'] if 'iss-last' in obj['article'] else ''
    meta.volumes.first = obj['article']['vol-first']
    meta.volumes.last = obj['article']['vol-last'] if 'vol-last' in obj['article'] else ''
    meta.publisher = obj['article']['imprintPublisher']['displayName']

    return meta


def map2(html):
    meta = Payload()
    td = html.find('title')
    if td:
        data = td.contents
        meta.title = data

    td = html.find('ul', {'class': 'authorGroup'})
    authors = {}
    affiliation = {}
    if td:
        for li in td.children:
            name = li.find_all('a')[0].contents[0]
            if li.find('sup'):
                reference = li.find('sup').contents[0]
            else:
                reference = 'a'
            authors[name] = reference

    td = html.find('ul', {'class': 'affiliation'})
    if td:
        for li in td.children:
            if li.find('sup'):
                reference = li.find('sup').contents[0]
            else:
                reference = 'a'
            institute = li.find('span').contents[0]
            affiliation[reference] = institute

    for author in authors:
        for institute in affiliation:
            if authors[author] == institute:
                meta.authors.append(Author(surname=author, affiliations=affiliation[institute]))

    td = html.find('p', {'class': 'volIssue'})
    (volume, issue) = td.find('a').contents[0].split(',')
    meta.volumes.first = volume.split()[-1]
    meta.issues.first = issue.split()[-1]
    (year, pages) = td.contents[-1].split(',')[1:3]
    pages = pages.split()[-1]
    m = re.search('([0-9]*).([0-9]*)', pages, re.UNICODE)
    pages = m.groups()
    meta.pages.first = pages[0]
    meta.pages.last = pages[1]
    td = html.find('div', {'class': 'title'})
    meta.journal_title = td.find('span').contents[0]
    meta.publisher = 'Elsevier'
    td = html.find('dl', {'class': 'articleDates'})
    data = td.find('dd').contents[0].split(',')
    accepted = ''
    online = ''
    received = ''
    for dates in data:
        if 'accepted' in dates.lower():
            m = re.search('([0-9]+.*[0-9]+)', dates)
            accepted = m.group(0)
        elif 'available' in dates.lower():
            m = re.search('([0-9]+.*[0-9]+)', dates)
            online = m.group(0)
        elif 'received' in dates.lower():
            m = re.search('([0-9]+.*[0-9]+)', dates)
            received = m.group(0)
    meta.online_date = online
    meta.publication_date = accepted
    meta.received = received
    td = html.find_all('script')
    for script in td:
        for element in script.contents:
            if 'doi' in element:
                for item in element.split(';'):
                    if 'SDM.doi' in item:
                        m = re.search("'(.*)'", item)
                        data = m.groups()
                        meta.doi = data[0]
    return meta
