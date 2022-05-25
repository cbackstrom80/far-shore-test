import argparse
import json
import os
import logging
import sys
import time
import pandas as pd
import asyncio
from random import randint, randrange
from datetime import datetime, timedelta
from IPython.display import display
import redis
redis = redis.Redis(
    host='0.0.0.0',
    port='6379')

# VARS ##
token = 'XnI5SWNNVv_uoCURsap5TA'
REALM = "us1"
randvalue = randrange(1000000, 9999999)




sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..'))
import signalfx  # noqa






#Send a Metric to Ingest
async def sendmetric(rando,token):
#TODO: TIME TO ACK
    client = signalfx.SignalFx(api_endpoint="https://api.{REALM}.signalfx.com".format(REALM = REALM),
                        ingest_endpoint="https://ingest.{REALM}.signalfx.com".format(REALM = REALM),
                        stream_endpoint='https://stream.{REALM}.signalfx.com'.format(REALM = REALM))
    ingest = client.ingest(token)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


    payload = ingest.send(gauges=[{
        'metric': 'nike.testing.metric',
        'value': rando}])
    return(time)


#Read The Metric from the API endpoint
async def getmetric(rando,token):
    import requests
    import json
    import pprint

    query = 'sf_metric:nike.testing.metric'
    base_url = 'https://api.us1.signalfx.com/v1/timeserieswindow?query='


    resp = requests.get(url=base_url + query,
                        headers={"Content-Type": "application/json", "X-SF-Token": token},
                        params=None)
    data = resp.json()  # Check the JSON Response Content documentation below



    for i in data['data']:
        for k in data['data'][i]:
            if rando == k[1]:
                #    print('Hulu is in the streaming service business')
                print(str(k[1]), str(k[0]))
                return(True)


#Report results back to SOS for charting purposes
async def reporttosfx(token,origin,diff ):
#TODO: TIME TO ACK
    client = signalfx.SignalFx(api_endpoint="https://api.{REALM}.signalfx.com".format(REALM = REALM),
                        ingest_endpoint="https://ingest.{REALM}.signalfx.com".format(REALM = REALM),
                        stream_endpoint='https://stream.{REALM}.signalfx.com'.format(REALM = REALM))
    ingest = client.ingest(token)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    origin="china"

    payload = ingest.send(cumulative_counters=[{
        'metric': 'nike.forshore.testing.result',
        'value': diff,
        'dimensions': {'origin': origin, 'realm': REALM}
            },
            ])
    return(payload)


#RUNNER
async def main():
    keys = ['ingress_start_time', 'api_time_to_console', 'time_delta']
    #record = {"ingress_start_time":[],"api_time_to_console":[],"time_delta":[]};
    record = []
    origin =""
    inc = 1
    index = 1
    df = pd.DataFrame({'start-time': 0, 'end-time': 0, 'latency': 0}, index=[index])
    df
    while inc == 1:
        task1 = asyncio.create_task(
            sendmetric(randvalue, token))
        task2 = asyncio.create_task(
            getmetric(randvalue, token))

        now = datetime.now()

        start_time = now.timestamp()
        print(f"started at {start_time}")


        await task1
        await task2
        now = datetime.now()
        end_time = now.timestamp()
        print(f"finished at {end_time}")
        #dfloop = pd.DataFrame(columns=[[start_time, end_time], 'MTS_SEND_TIME', 'MTS_GET_TIME'], index=['x', 'y'])
        #df.append(dfloop, ignore_index=True)
        #print(df)
        diff = (start_time - end_time)
        print("Difference in time is: {} ms.".format(diff))
        #record = record.append(start_time,end_time,diff)
        #print(record)

        index = index + 1
        #testps = pd.DataFrame.iloc[1]({'start-time':start_time,'end-time':end_time,'latency':diff},index=[index])
        #df.iloc[+1] = {'start-time':start_time,'end-time':end_time,'latency':diff}
        redis.set('farshore_test_'+ str(index), json.dumps({'start-time':float(start_time),'end-time':float(end_time),'latency':float(diff)}))
        farshore = redis.keys('farshore_test*')
        print(farshore)
        sendtosfx = asyncio.create_task(

            reporttosfx(token,origin, diff))
        await sendtosfx



        time.sleep(1)

#TODO ADD SPAN TEST
#TODO ADD PERFORMANCE
#TODO % of failures/retrys
#TODO META FOR ORIGIN
#TODO OTEL COLLECTOR AND DOCKER COMPOSE

















asyncio.run(main())

