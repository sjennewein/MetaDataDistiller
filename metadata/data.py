import json
import requests
from metadata import wiley
from metadata import worldscientific
from metadata import jpharmsci
from metadata import hindawi
from metadata import elsevier
from metadata import springer
from metadata import nature
from metadata import ieee
from metadata import iucr

def extract(doi, type=None):
    metadata = {}
    url = ''

    if type == 'url':
        doc_url = doi.rstrip()
    else:
        url = 'http://doi.org/api/handles/' + doi.rstrip()

    if not type:
        try:
            r = requests.get(url)
        except:
            return {}
        content = json.loads(r.content.decode())
        r.close()

        if 'values' in content.keys():
            for element in content['values']:
                if element['type'] == 'URL':
                     doc_url = element['data']['value']
        else:
            print('return')
            return metadata

    #print(doc_url)
    if 'wiley' in doc_url:
        metadata = wiley.map(doc_url)
    elif 'worldscientific' in doc_url:
        metadata = worldscientific.map(doc_url)
    elif 'jpharmsci' in doc_url:
        metadata = jpharmsci.map(doc_url)
    elif 'hindawi' in doc_url:
        metadata = hindawi.map(doc_url)
    elif 'elsevier' in doc_url:
        metadata = elsevier.map(doc_url)
    elif 'springer' in doc_url:
        metadata = springer.map(doc_url)
    elif 'nature' in doc_url:
        metadata = nature.map(doc_url)
    elif 'ieee' in doc_url:
        metadata = ieee.map(doc_url)
    elif 'iucr' in doc_url:
        metadata = iucr.map(doc_url)
    return metadata
