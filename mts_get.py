import requests
import json
import pprint


query = 'sf_metric:nike.testing.metric AND randomvalue:7420942'
base_url = 'https://api.us1.signalfx.com/v1/timeserieswindow?query='
concat_url = query + base_url





resp = requests.get(url=base_url + query, headers={"Content-Type": "application/json","X-SF-Token": "XnI5SWNNVv_uoCURsap5TA"},params=None)
data = resp.json() # Check the JSON Response Content documentation below



rando = 7420942

for i in data['data']:
    for k in data['data'][i]:
        if rando == k[1]:

            print(str(k[1]),str(k[0]))



            """

for i in data['data']:
    for k in data['data'][i]:
        print(k)
        if rando == k[1]:

        print(str(k[1]),str(k[0]))"""


