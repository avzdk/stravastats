#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Last Modified: 2022/11/10 12:06:37


from flask import Flask, request, stream_with_context, render_template
from statsgenerator import stravaClient, StatsGenerator, Activity
from datetime import date

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
client = stravaClient()


def filter(args):
    startDateArray = args.get("startDate").split("-")
    endDateArray = args.get("endDate").split("-")
    distanceMin = float(args.get("distanceMin"))
    distanceMax = float(args.get("distanceMax"))

    global sg
    sg.reset()
    sg.filter(lambda a: a.distance >= distanceMin)
    sg.filter(lambda a: a.distance <= distanceMax)
    sg.filter(
        lambda a: a.date
        >= date(int(startDateArray[0]), int(startDateArray[1]), int(startDateArray[2]))
    )
    sg.filter(
        lambda a: a.date
        <= date(int(endDateArray[0]), int(endDateArray[1]), int(endDateArray[2]))
    )


@app.route("/")
def home():
    if client.access_token == None:
        return render_template("login.html")
    else:
        return render_template(
            "stats.html", data=sg.activities_work, stats=sg.basicstats()
        )


@app.route("/filter")
def filter2():
    filter(request.args)
    return render_template("stats.html", data=sg.activities_work, stats=sg.basicstats())


@app.route("/chart")
def chart():
    filter(request.args)
    global sg

    x = []
    y = []
    weeklystats = sg.weeklystats()
    for week in weeklystats:
        x.append("w" + week)
        y.append(weeklystats[week])

    return render_template("chart.html", x=x, y=y, stats=sg.basicstats())


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


if __name__ == "__main__":

    app.run()
