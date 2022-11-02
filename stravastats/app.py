#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Last Modified: 2022/11/02 12:08:36


from flask import Flask, request, stream_with_context, render_template
from statsgenerator import stravaClient, statsGenerator, Activity
from datetime import date

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
client=stravaClient()

@app.route('/')
def home():
    sg.reset()
    return render_template('index.html', data=sg.activities_work, stats=sg.basicstats())

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/exchange_token')
def exchange_token():
    authorization_code = request.args.get('code')
    scope = request.args.get('scope')
    print(f"Modtaget autorization_code  {authorization_code}")
    client.exchange(authorization_code)

    global sg
    activities=[]
    for activity in client.runningactivities(after_date=date(2022,1,1)):
        dc=Activity(activity['start_date_local'],activity['name'],activity['distance'],activity['moving_time'],activity['average_speed'],activity['sport_type'])
        activities.append(dc)
    sg=statsGenerator(activities)
    

    return (f"OK! code:{authorization_code} scope:{scope}")
    

@app.route('/halfmarathons')
def p_halfmarathons(): 
    sg.reset()
    sg.filter(lambda a: a.distance > 21000)
    sg.sort(lambda a: -a.tempo)
    print(sg.activities_work[1])
    return render_template('index.html', data=sg.activities_work)

if __name__ == '__main__':

    app.run()
