#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Last Modified: 2022/11/10 12:06:37


from flask import Flask, request, stream_with_context, render_template
from statsgenerator import stravaClient, StatsGenerator, Activity
from datetime import date

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
client = stravaClient()


def use_filter(args):
    global sg
    sg.reset()
    if len(args) > 0:
        startDateArray = args.get("startDate").split("-")
        endDateArray = args.get("endDate").split("-")
        distanceMin = float(args.get("distanceMin"))
        distanceMax = float(args.get("distanceMax"))
        sg.filter(lambda a: a.distance >= distanceMin)
        sg.filter(lambda a: a.distance <= distanceMax)
        sg.filter(
            lambda a: a.date
            >= date(
                int(startDateArray[0]), int(startDateArray[1]), int(startDateArray[2])
            )
        )
        sg.filter(
            lambda a: a.date
            <= date(int(endDateArray[0]), int(endDateArray[1]), int(endDateArray[2]))
        )


@app.route("/exchange_token")
def exchange_token():
    authorization_code = request.args.get("code")
    scope = request.args.get("scope")
    print(f"Modtaget autorization_code  {authorization_code}")
    client.exchange(authorization_code)

    # global sg
    # sg = StatsGenerator(client.runningactivities())
    # return render_template("stats.html", data=sg.activities_work, stats=sg.basicstats())
    return render_template("athlete.html", data=client.getAthlete())


@app.route("/loaddata")
def loaddata():
    global sg
    sg = StatsGenerator(client.runningactivities())
    return "ok"


@app.route("/")
def home():
    return render_template("login.html")

    # if client.access_token == None:

    # else:
    #    return render_template(
    #        "stats.html", data=sg.activities_work, stats=sg.basicstats()
    #    )


@app.route("/filter")
def filter():

    use_filter(request.args)
    return render_template("stats.html", data=sg.activities_work, stats=sg.basicstats())


@app.route("/chart")
def chart():
    use_filter(request.args)
    global sg
    # bar hcart by weeks
    bar_x = []
    bar_y = []
    weeklystats = sg.weeklystats()
    for week in weeklystats:
        bar_x.append("w" + week)
        bar_y.append(weeklystats[week])

    # scatterplot
    scat_x = []
    scat_y = []
    for a in sg.activities_work:
        scat_x.append(a.distance)
        scat_y.append(a.tempo)

    return render_template(
        "chart.html",
        bar_x=bar_x,
        bar_y=bar_y,
        scat_x=scat_x,
        scat_y=scat_y,
        stats=sg.basicstats(),
    )


@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":

    app.run()
