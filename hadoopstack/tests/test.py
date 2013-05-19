import os
del os.environ['http_proxy']

import requests
import json
url = "http://localhost:5000/v1/clusters/"
#data = {'sender': 'Alice', 'receiver': 'Bob', 'message': 'We did it!'}
data={'cluster':{'name':'test','node-recipes':{"jobtracker":1,"tasktracker":3},'image-id': 'ubuntu-12.04-amd64.img'}}
data_string = json.dumps(data)
print data_string

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)
print r.text


########curl script for the same
#curl --dump-header  -v -H "Accept: application/json" -H "Content-Type: application/json" -X POST --data "{\"uid\":12,\"token\":\"asdert\"}" http://localhost:5000/v1/

