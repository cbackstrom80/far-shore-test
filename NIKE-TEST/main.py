import asyncio
import json
import time
from typing import Dict, Any, List, Tuple
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from itertools import repeat
from aiohttp import ClientSession
import signalfx
import sys
import os
import logging
from random import randint, randrange
from datetime import datetime, timedelta

########  VARIABLES ##########
import yaml
with open("far-shore-config.yaml", "r") as yamlfile:
     data = yaml.load(yamlfile, Loader=yaml.FullLoader)
     print("Config Loaded Successfully  ")
REALM = data['farshore']['app']['options']['test-target-realm']
LOCALE = data['farshore']['app']['options']['test-src-locale']
METRICBASENAME = data['farshore']['app']['options']['test-metric-base-name']
TOKEN = data['farshore']['app']['options']['token']
OTELCOLLECTORINGEST = data['farshore']['app']['options']['otelcollectoringest']
SFXAPIURL = data['farshore']['app']['options']['sfx-api-url']





def http_get_with_requests(url: str, headers: Dict = {}, proxies: Dict = {}, timeout: int = 10) -> (int, Dict[str, Any], bytes):
    response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)

    response_json = None
    try:
        response_json = response.json()
    except:
        pass

    response_content = None
    try:
        response_content = response.content
    except:
        pass

    return (response.status_code, response_json, response_content)
def http_get_with_requests_parallel(list_of_urls: List[str], headers: Dict = {}, proxies: Dict = {}, timeout: int = 10) -> (List[Tuple[int, Dict[str, Any], bytes]], float):
    t1 = time.time()
    results = []
    executor = ThreadPoolExecutor(max_workers=100)
    for result in executor.map(http_get_with_requests, list_of_urls, repeat(headers), repeat(proxies), repeat(timeout)):
        results.append(result)
    t2 = time.time()
    t = t2 - t1
    return results, t
async def http_get_with_aiohttp(session: ClientSession, url: str, headers: Dict = {}, proxy: str = None, timeout: int = 10) -> (int, Dict[str, Any], bytes):
    response = await session.get(url=url, headers=headers, proxy=proxy, timeout=timeout)
    print('-----------')
    print('-----------')
    print('-----------')
    print('-----------')
    print('-----------')
    print(response.status)

    response_json = None
    try:
        response_json = await response.json(content_type=None)
    except json.decoder.JSONDecodeError as e:
        pass

    response_content = None
    try:
        response_content = await response.read()
    except:
        pass

    return (response.status, response_json, response_content)
async def sendmetric(randvalue):


    # TODO: TIME TO ACK
    client = signalfx.SignalFx(api_endpoint=SFXAPIURL,
                               ingest_endpoint=OTELCOLLECTORINGEST)
    ingest = client.ingest(TOKEN)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    now = datetime.now()

    start_time = now.timestamp()
    payload = ingest.send(gauges=[{
        'metric': METRICBASENAME,
        'value': start_time,
        'dimensions': {'source-locale': LOCALE,
                       'realm': REALM,
                       'randomvalue':str(randvalue)
                       }
    }])
    return (True)

def post_results_to_sfx(avg_speed,LOCALE,REALM):


    # TODO: TIME TO ACK
    client = signalfx.SignalFx(api_endpoint=SFXAPIURL,
                               ingest_endpoint=OTELCOLLECTORINGEST)
    ingest = client.ingest(TOKEN)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    now = datetime.now()

    start_time = now.timestamp()
    payload = ingest.send(gauges=[{
        'metric': 'nike.farshore.testing.avg_time_seconds',
        'value': avg_speed,
        'dimensions': {
                    'source-locale': LOCALE,
                       'realm': REALM,
                      #'timetoglass': str(100),

                }
    }])
    return (True)

async def http_get_with_aiohttp_parallel(randvalue, session: ClientSession, list_of_urls: List[str], headers: Dict = {"Content-Type": "application/json", "X-SF-Token": TOKEN}, proxy: str = None, timeout: int = 10) -> (List[Tuple[int, Dict[str, Any], bytes]], float):
    print('debug URLS')
    print(list_of_urls)
    print('--------------')
    print('debug Headers')
    print(headers)
    print('--------------')

    t1 = time.time()
    results1 =await asyncio.create_task(sendmetric(randvalue))
    results2 = await asyncio.gather(*[http_get_with_aiohttp(session, url, headers, proxy, timeout) for url in list_of_urls])
    t2 = time.time()
    t = t2 - t1

    return results1,results2, t


async def main():

    print('Waiting 20seconds for Collector to come online')
    print('--------------------')
    time.sleep(20)



    # Benchmark aiohttp
    session = ClientSession()
    speeds_aiohttp = []
    randvalue = randrange(1000000, 9999999)
    for i in range(0, 1):

        urls = [
            "https://api.us0.signalfx.com/v1/timeserieswindow?query=sf_metric:nike.testing.metric AND randomvalue:{}".format(randvalue)
            for i in range(0, 10)]
        results1, results2, t = await http_get_with_aiohttp_parallel(randvalue,  session, urls)
        print(results2)
        v = len(urls) / t
        print('AIOHTTP: Took ' + str(round(t, 2)) + ' s, with speed of ' + str(round(v, 2)) + ' r/s')
        speeds_aiohttp.append(v)
        ttg=round(t, 2)
    await session.close()

    print('--------------------')



    # Calculate averages
    avg_speed_aiohttp = sum(speeds_aiohttp) / len(speeds_aiohttp)

    print('--------------------')
    print('AVG ROUNDTRIO SPEED USING AIOHTTP: ' + str(round(avg_speed_aiohttp, 2)) + ' r/s')

    post_results_to_sfx(ttg,LOCALE,REALM)
while 1==1:
    asyncio.run(main())
