#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Last Modified: 2022/11/29 11:08:58


from datetime import date

from flask import Flask, render_template, request, stream_with_context
from statsgenerator import Activity, StatsGenerator, stravaClient

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
client = stravaClient()


def use_filter(args):
    global sg
    sg.reset()
    if len(args) > 0:
        startDateArray = args.get("startDate", default="2000-01-01").split("-")
        endDateArray = args.get("endDate", default="2030-01-01").split("-")
        distanceMin = float(args.get("distanceMin", default=0))
        distanceMax = float(args.get("distanceMax", default=1000))
        tempoMin = args.get("tempoMin", default="00:00")
        tempoMax = args.get("tempoMax", default="59:00")
        sg.filter(lambda a: a.distance >= distanceMin)
        sg.filter(lambda a: a.distance <= distanceMax)
        sg.filter(lambda a: a.tempo_in_txt >= tempoMin)
        sg.filter(lambda a: a.tempo_in_txt <= tempoMax)
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

@app.route("/stravastats/")
def hello():
    print("xxxxxxxxxxxxxxxxxxxxx")
    return "<h1 style='color:blue'>Hellodffsdf There 666!</h1>"

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
        bar_y.append(weeklystats[week]["distance_sum"])

    # scatterplot
    scat_x = []
    scat_y = []
    scat_text = []
    for a in sg.activities_work:
        scat_x.append(a.distance)
        scat_y.append(a.tempo)

        scat_text.append(a.date.strftime("%m/%d/%Y") + " id:" + a.stravaid)

    return render_template(
        "chart.html",
        bar_x=bar_x,
        bar_y=bar_y,
        scat_x=scat_x,
        scat_y=scat_y,
        scat_text=scat_text,
        stats=sg.basicstats(),
    )


@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":

    app.run()
