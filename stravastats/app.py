#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Last Modified: 2022/11/10 12:06:37


from flask import Flask, request, stream_with_context, render_template
from statsgenerator import stravaClient, StatsGenerator, Activity
from datetime import date

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
client = stravaClient()


@app.route("/")
def home():
    if client.access_token == None:
        return render_template("login.html")
    else:
        return render_template(
            "stats.html", data=sg.activities_work, stats=sg.basicstats()
        )


@app.route("/filter")
def filter():
    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")
    distanceMin = float(request.args.get("distanceMin"))
    distanceMax = float(request.args.get("distanceMax"))
    print(f"--------ARGUMENTER -------- {distanceMin} {distanceMax} ")
    global sg
    sg.reset()
    sg.filter(lambda a: a.distance >= distanceMin)
    sg.filter(lambda a: a.distance <= distanceMax)
    return render_template("stats.html", data=sg.activities_work, stats=sg.basicstats())


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/exchange_token")
def exchange_token():
    authorization_code = request.args.get("code")
    scope = request.args.get("scope")
    print(f"Modtaget autorization_code  {authorization_code}")
    client.exchange(authorization_code)

    global sg
    sg = StatsGenerator(client.runningactivities())

    return render_template("stats.html", data=sg.activities_work, stats=sg.basicstats())


@app.route("/halfmarathons")
def p_halfmarathons():
    sg.reset()
    sg.filter(lambda a: a.distance > 21)
    sg.sort(lambda a: -a.tempo)
    return render_template("stats.html", data=sg.activities_work, stats=sg.basicstats())


if __name__ == "__main__":

    app.run()
