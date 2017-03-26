import requests

def map(doi):
    url = 'http://api.crossref.org/works/' + doi

    try:
        r = requests.get(url)
    except:
        return {}

    r.close()
    r.raise_for_status()

    metadata = r.json()
    metadata['source'] = 'crossref'

    return metadata