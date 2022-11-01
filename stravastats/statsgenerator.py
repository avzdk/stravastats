#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Last Modified: 2022/11/01 11:26:29
from dataclasses import dataclass
from strava import Strava
from datetime import datetime,date,timedelta
from pprint import pp

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

    def runningactivities(self):
        # henter alle aktiviteter ved at kalde API flere gange indtil der ikke er flere.
        # filtrerer desuden så det kun er løb.
        self.getToken()
        activities=[]  
        for page in range(1,500):
            rv=self.getActivities(100,page,datetime.combine(date(2022,1,1),datetime.min.time()))
            if rv != []: activities=activities+rv
            else: break     
        print(f"ANTAL {len(activities)} hentet")       
        for a in activities:
            if a['sport_type']!='Run':
                activities.remove(a)
        print(f"ANTAL {len(activities)} efter filtrering på løb")     
        return activities

class statsGenerator():
    def __init__(self,rawdata): 
        self.rawdata = rawdata
        for activity in self.rawdata: #
            activity.date=datetime.strptime(activity.start_date_local[0:10], "%Y-%m-%d").date()
        self.activities = rawdata       # de data der arbejdet på efter filtrering
        # start_date,start_date_local,distance,moving_time,average_speed,max_speed,average_cadance,
        self._group_by_date()
        
    def _group_by_date(self):
        pass
    
    def sort_distance(self):
        newlist = sorted(self.activities, key=lambda d: -d.distance) 
        return newlist

    def filter_distance(self,min=0,max=100000): # i meter
        self.activities=[activity for activity in self.activities if activity.distance >= min and activity.distance <= max]
        return self.activities

    def sort_tempo(self):
        newlist = sorted(self.activities, key=lambda d: d.tempo) 
        return newlist

        
if __name__ == '__main__':
    client=stravaClient()
    activities_main:list[Activity] = []  # samtlige aktiviteter. 
    activities_work:list[Activity] = []  # filtrerede aktiviteter til analyse. Overskrives løbende.
    for activity in client.runningactivities():
        dc=Activity(activity['start_date_local'],activity['name'],activity['distance'],activity['moving_time'],activity['average_speed'],activity['sport_type'])
        activities_main.append(dc)

    activities_work= [a for a in activities_main if (a.distance>6000)]

    #activities_work= list(filter(lambda a: a.distance > 6000, activities))
    pp(activities_main)
    pp(len(activities_main))
    pp(len(activities_work))


    #statsgenerator=statsGenerator(activities)
    #hm=statsgenerator.filter_distance(min=5000,max=6000)
    #print(hm)
#    longest=statsgenerator.sort_distance()
#    print(longest[0])
    #fastest=statsgenerator.sort_tempo()
    #print(fastest[:3])