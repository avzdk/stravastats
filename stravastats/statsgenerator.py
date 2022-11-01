#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Last Modified: 2022/11/01 13:11:31
from dataclasses import dataclass
from strava import Strava
from datetime import datetime,date,timedelta
from pprint import pp
import logging

log = logging.getLogger(__name__)

log.info("Start")


@dataclass
class Activity:
    start_date_local : str
    name : str
    distance : float        # meter
    moving_time: float
    average_speed: float    
    sport_type : str
    date : datetime = None

    @property
    def tempo(self):        # minutter
        return 1/self.average_speed*1000/60
    
    @property
    def tempo_in_txt(self):
        return str(timedelta(minutes=self.tempo))[2:7]

    def __repr__(self):
        return f"Activity({self.date}  {self.distance/1000:.2f} km   {self.name}  {self.moving_time/60:.2f} min. Tempo:{self.tempo:.2f})\n"

    


class stravaClient(Strava):

    def runningactivities(self,after_date:date=date(1974,1,1)):
        # henter alle aktiviteter ved at kalde API flere gange indtil der ikke er flere.
        # filtrerer desuden så det kun er løb.
        self.getToken()
        activities=[]  
        for page in range(1,500):
            rv=self.getActivities(200,page,datetime.combine(after_date,datetime.min.time()))
            if rv != []: activities=activities+rv
            else: break     
        log.info(f"ANTAL {len(activities)} hentet")       
        activities= list(filter(lambda a: a['sport_type']=='Run', activities))
        log.info(f"heraf {len(activities)} løb")       
        activities= list(filter(lambda a: a['distance']>1, activities))
        log.info(f"efter fjernelse af dist=0 : {len(activities)} ")       
        return activities

class statsGenerator():
    def __init__(self,activities_main): 
        self.activities_main = activities_main
        self.reset()

    def reset(self):
        # vender tilbage til den samlede liste af løb.
        self.activities_work = self.activities_main.copy()
    
    def filter(self,filterfunction):
        # filtrerer og overskriver activities_work
        # Eksempel på anvendelse statsgenerator.filter(lambda a: a.distance > 15000)
        self.activities_work= list(filter(filterfunction, self.activities_work))

    def sort(self,sortfunction):
        # sorterer og overskriver activities_work
        # Eksempel på anvendelse statsgenerator.sort(lambda a: -a.distance)
        self.activities_work= list(sorted(self.activities_work, key=sortfunction))

    def basicstats(self):
        distance_max=max( statsgenerator.activities_work, key=lambda a: a.distance)
        distance_min=min( statsgenerator.activities_work, key=lambda a: a.distance)
        tempo_max=max( statsgenerator.activities_work, key=lambda a: a.tempo)
        tempo_min=min( statsgenerator.activities_work, key=lambda a: a.tempo)

        stats={}
        stats['distance_max']=distance_max.distance
        stats['distance_min']=distance_min.distance
        stats['tempo_max']=tempo_max
        stats['tempo_min']=tempo_min
        return(stats)
        

    
        
if __name__ == '__main__':
    client=stravaClient()
    activities:list[Activity] = []  # samtlige aktiviteter. 
    for activity in client.runningactivities(after_date=date(2022,1,1)):
        dc=Activity(activity['start_date_local'],activity['name'],activity['distance'],activity['moving_time'],activity['average_speed'],activity['sport_type'])
        activities.append(dc)

    statsgenerator=statsGenerator(activities)
    print(len(statsgenerator.activities_work))
    statsgenerator.filter(lambda a: a.distance > 15000)
    statsgenerator.sort(lambda a: -a.distance)
    print(len(statsgenerator.activities_work))
    pp(statsgenerator.activities_work)

    print(statsgenerator.basicstats())

    