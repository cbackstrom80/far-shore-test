import argparse
import json
import os
import logging
import sys
import time
#import pandas as pd
import asyncio
from random import randint, randrange
from datetime import datetime, timedelta

########  VARIABLES ##########
import yaml
with open("far-shore-config.yaml", "r") as yamlfile:
     data = yaml.load(yamlfile, Loader=yaml.FullLoader)
     print("Read successful")

latencymeasure = data['farshore']['app']['options']['latency-measure']


import redis
redis = redis.Redis(
    host='redis',
    port='6379')

# VARS ##
token = 'XnI5SWNNVv_uoCURsap5TA'
REALM = "us1"

otelingest = "http://splunk-otel-collector:9943"




sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..'))
import signalfx  # noqa



##### CLASS FOR HANDLING SENDING DATA INTO ####
class sfxroundtrip:

    def sendmetric(token, otelingest, start_time):


        # TODO: TIME TO ACK
        client = signalfx.SignalFx(api_endpoint="https://api.{REALM}.signalfx.com".format(REALM=REALM),
                                   ingest_endpoint=otelingest,
                                   stream_endpoint='https://stream.{REALM}.signalfx.com'.format(REALM=REALM))
        ingest = client.ingest(token)
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        print(type(start_time))


        payload = ingest.send(gauges=[{
            'metric': 'nike.testing.metric',
            'value': start_time,
            'dimensions': {'source-locale': data['farshore']['app']['options']['test-src-local'],
                           'realm': data['farshore']['app']['options']['test-target-realm']
                           }
        }])
        return (True)

        # Read The Metric from the API endpoint
    def getmetric(rando, token):
        import requests
        import json
        import pprint

        match = 0
        while match == 0:
            try:
                query = 'sf_metric:nike.testing.metric AND randomvalue:{}'.format(rando)
                base_url = 'https://api.us1.signalfx.com/v1/timeserieswindow?query='

                resp = requests.get(url=base_url + query,
                                    headers={"Content-Type": "application/json", "X-SF-Token": token},
                                    params=None)
                data = resp.json()  # Check the JSON Response Content documentation below
                for i in data['data']:
                    for k in data['data'][i]:
                        print("Looking for metric number: {}".format(rando))
                        print(k)
                        if rando == k[1]:
                            print(str(k[1]), str(k[0]))
                            print("Weve Found a Match!  Carry on!")
                            match = 1
                            return (True)
            except:
                "Try Again"




    def trip(randvalue, token, otelingest):
        if sfxroundtrip.sendmetric(randvalue, token, otelingest) == True:
            if sfxroundtrip.getmetric(randvalue, token) == True:




                read_time = datetime.now()

                # TODO: TIME TO ACK
                client = signalfx.SignalFx(api_endpoint="https://api.{REALM}.signalfx.com".format(REALM=REALM),
                                           ingest_endpoint=otelingest,
                                           stream_endpoint='https://stream.{REALM}.signalfx.com'.format(REALM=REALM))
                ingest = client.ingest(token)
                logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
                print("Test Start Time is {}".format(sfxroundtrip.start_time))
                print("Test End Time is {}".format(read_time))




                diff = read_time - sfxroundtrip.start_time
                value = diff.total_seconds() * 1000

                print("The Time To Glass is {}".format(diff.total_seconds()))
                payload = ingest.send(gauges=[{
                    'metric': 'nike.testing.result',
                    'value': value,
                    'dimensions': {'origin': "NIKE-CN", 'realm': REALM, 'ingest_start': str(sfxroundtrip.start_time),
                                   'read_time': str(read_time), }
                },
                ])























#Report results back to SOS for charting purposes



#RUNNER
class async_farshore_test:
    async def main():
        keys = ['ingress_start_time', 'api_time_to_console', 'time_delta']
        #record = {"ingress_start_time":[],"api_time_to_console":[],"time_delta":[]};
        record = []
        origin =""
        inc = 1
        index = 1


        while inc == 1:
            randvalue = randrange(1000000, 9999999)
            task1 = asyncio.create_task(sendmetric(randvalue, token, otelingest))
            #task2 = asyncio.create_task(getmetric(randvalue, token))

            now = datetime.now()

            start_time = now.timestamp()
            print(f"started at {start_time}")


            await task1
            #await task2
            now = datetime.now()
            end_time = now.timestamp()
            print(f"finished at {end_time}")

            diff = (start_time - end_time)
            print("Difference in time is: {} ms.".format(diff))


            index = index + 1


            #redis.set('farshore_test_'+ str(index), json.dumps({'start-time':float(start_time),'end-time':float(end_time),'latency':float(diff)}))
            #farshore = redis.keys('farshore_test*')
            #print(farshore)
            sendtosfx = asyncio.create_task(reporttosfx(token,origin, diff,sendmetric(randvalue, token, otelingest),getmetric(randvalue, token)))
            await sendtosfx



            time.sleep(1)

#TODO ADD SPAN TEST
#TODO ADD PERFORMANCE
#TODO % of failures/retrys
#TODO META FOR ORIGIN
#TODO OTEL COLLECTOR AND DOCKER COMPOSE




"""def farshore_test_and_report():
    inc = 1
    origin = "NIKE-CN"

    randvalue = randrange(1000000, 9999999)
    sfxroundtrip.trip(randvalue,token,otelingest)
    time.sleep(1)


farshore_test_and_report()"""

time.sleep(20)
while 1 == 1: # FOREVER
    sfxroundtrip.sendmetric(token, otelingest, datetime.now().timestamp())
    time.sleep(1)




#asyncio.run(main())

