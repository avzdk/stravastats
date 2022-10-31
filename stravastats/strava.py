#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Last Modified: 2022/06/21 21:34:14

'''
Wrapper til Strava.

Se mere på
https://github.com/franchyze923/Code_From_Tutorials/blob/master/Strava_Api/strava_api.py
https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde
https://developers.strava.com/docs/reference/#api-Activities-getLoggedInAthleteActivities
'''

import requests
import urllib3
import logging
import configparser
import os
from datetime import date,datetime
from pprint import pp

ENVIRONMENT = os.environ.get("ENV", "local")
print(f"env:{ENVIRONMENT}")
conf = configparser.ConfigParser()
if ENVIRONMENT == "local":
    cf = conf.read(os.path.join(os.path.dirname(__file__),"config_local.ini"))
else:
    cf = conf.read(os.path.join(os.path.dirname(__file__),"config.ini"))

log = logging.getLogger(__name__)
logging.basicConfig(
    level=conf.get("LOG", "LEVEL", fallback="DEBUG"),
    format="%(levelname)s %(module)s.%(funcName)s %(message)s",
)
log.info(
    f"Starting service loglevel={conf['LOG']['LEVEL']} @ {ENVIRONMENT} environemnt "
)
log.info(f"WorkingDirectory: {os.getcwd()}")
log.info(f"Configurationfiles: {cf}")

CLIENT_ID=conf['STRAVA']['client_id']
CLIENT_SECRET=conf['STRAVA']['client_secret']
REFRESH_TOKEN=conf['STRAVA']['refresh_token']




class Strava():
    def __init__(self):
        self.auth_url = "https://www.strava.com/oauth/token"
        self.activites_url = "https://www.strava.com/api/v3/athlete/activities"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def getToken(self):
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': REFRESH_TOKEN,
            'grant_type': "refresh_token",
            'f': 'json'
        }
        res = requests.post(self.auth_url, data=payload, verify=False)
        pp(res.json())
        self.access_token = res.json()['access_token']
        

    def getActivities(self,pagesize=200,page=1, after:datetime =datetime.combine(date(1974,1,1),datetime.min.time())):
        
        # det ladet til at 200 pr. side er maximum
        header = {'Authorization': 'Bearer ' + self.access_token}
        param = {'per_page': pagesize, 'page': page, 'after':after.timestamp() }
        activities = requests.get(self.activites_url, headers=header, params=param).json()
        return activities
        

if __name__ == "__main__":
    client=Strava()
    client.getToken()
    activities = client.getActivities(10)
    for a in activities:
        pp(a['name'])












