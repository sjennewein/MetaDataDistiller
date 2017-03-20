import re
import urllib.parse
import glob
import os
import time
from metadata import data 
import json
import requests
import zipfile
import sys

def touch(fname):
    with open(fname,'a'):
        os.utime(fname,None)

input = sys.argv[1]
output = sys.argv[2]

input = os.path.expanduser(input)
output = os.path.expanduser(output)

touch(output + 'missed.log')

try:
    os.makedirs(output)
except:
#    print('exist')
    pass

with open(input) as f:
    content = f.readlines()

content = [x.strip() for x in content]

total_time = time.time()
for doi in content:
        start_time = time.time()

        metadata = data.extract(doi)

        registrar  = doi.split('/')[0]
        try:
            os.stat(output+registrar)
        except:
            os.mkdir(output+registrar)

        if not metadata:
            with open(output + 'missed.log','a') as f:
                f.write(doi + '\n')
            continue

        with open(output + doi, 'w') as json_file:
            json_file.write(json.dumps(metadata))

        print("--- %s seconds ---" % (time.time() - start_time))


print("--- TOTAL: %s seconds ---" % (time.time() - total_time))
