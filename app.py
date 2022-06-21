#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Last Modified: 2022/06/21 22:10:41


from flask import Flask, stream_with_context, render_template
from statsgenerator import stravaClient, statsGenerator, Activity


app = Flask(__name__)
client=stravaClient()

@app.route('/')
def home():
    hm=statsgenerator.filter_distance(min=5000,max=6000)
    return render_template('index.html', data=hm)


@app.route('/halfmarathons')
def p_halfmarathons():
    print("HM1")
    hm=statsgenerator.filter_distance(min=20500,max=60000)
    return render_template('index.html', data=hm)
    print("HM2")


if __name__ == '__main__':
    
    activities=[]
    for activity in client.runningactivities():
        dc=Activity(activity['start_date_local'],activity['name'],activity['distance'],activity['moving_time'],activity['average_speed'],activity['sport_type'])
        activities.append(dc)
    statsgenerator=statsGenerator(activities)
    app.run()

