from unittest import TestCase
from metadata import data
from metadata.payload import PayloadEncoder, Payload
import json


class TestPayload(TestCase):
    def test_payloadEncoder(self):
        data = Payload()
        jdata = PayloadEncoder().encode(data)
        newData = json.loads(jdata)
        self.assertEqual(type(newData['issues']), dict)
        self.assertEqual(type(newData['authors']), list)


class TestExtract(TestCase):
    def test_RealWorld(self):
        with open('random_doi', 'r') as infile:
            doi_list = infile.readlines()
        # doi_list = [ '10.1016/0022-5193%2872%2990196-8',]
        i = 0
        for doi in doi_list:
            dl = data.extract(doi.rstrip())
            with open(str(i) + '.json','w') as outfile:
                outfile.write(PayloadEncoder().encode(dl))
            self.assertNotEqual(dl,{})
            i += 1
        pass
