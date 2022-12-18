#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Last Modified: 2022/11/29 11:08:58


from datetime import date

from flask import Flask, render_template, request, stream_with_context
from statsgenerator import Activity, StatsGenerator, stravaClient
import logging
import configparser
import os
from datetime import datetime

ENVIRONMENT = os.environ.get("ENV", "local")
print(f"env:{ENVIRONMENT}")
conf = configparser.ConfigParser()
if ENVIRONMENT == "local":
    cf = conf.read(os.path.join(os.path.dirname(__file__), "config_local.ini"))
else:
    cf = conf.read(os.path.join(os.path.dirname(__file__), "config.ini"))

log = logging.getLogger(__name__)
log.info("Start")


logging.basicConfig(
    level=conf.get("LOG", "LEVEL", fallback="DEBUG"),
    format="%(levelname)s %(module)s.%(funcName)s %(message)s",
)
log.info(
    f"Starting service loglevel={conf['LOG']['LEVEL']} @ {ENVIRONMENT} environemnt "
)
log.info(f"WorkingDirectory: {os.getcwd()}")
log.info(f"Configurationfiles: {cf}")


URLPREFIX = conf["WWWSERVER"]["url_prefix"]
SERVER = conf["WWWSERVER"]["server"]

app = Flask(__name__, static_url_path=URLPREFIX + "/static")
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


@app.route(URLPREFIX + "/alive/")
def hello():

    return f"""
    time: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} </br>
    server: {SERVER} </br>
    urlprefix: {URLPREFIX} </br>
    environement: {ENVIRONMENT} </br>
    workingdir: {os.getcwd()} </br>
    conf.files: {cf} </br>
    </h1>"""


@app.route(URLPREFIX + "/exchange_token")
def exchange_token():
    authorization_code = request.args.get("code")
    scope = request.args.get("scope")
    print(f"Modtaget autorization_code  {authorization_code}")
    client.exchange(authorization_code)

    # global sg
    # sg = StatsGenerator(client.runningactivities())
    # return render_template("stats.html", data=sg.activities_work, stats=sg.basicstats())
    return render_template("athlete.html", data=client.getAthlete())


@app.route(URLPREFIX + "/loaddata")
def loaddata():
    global sg
    sg = StatsGenerator(client.runningactivities())

    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


@app.route(URLPREFIX + "/")
@app.route("/")
def home():
    return render_template(
        "login.html",
        redirecturi=SERVER + URLPREFIX + "/exchange_token",
    )

    # if client.access_token == None:

    # else:
    #    return render_template(
    #        "stats.html", data=sg.activities_work, stats=sg.basicstats()
    #    )


@app.route(URLPREFIX + "/filter")
def filter():

    use_filter(request.args)
    return render_template("stats.html", data=sg.activities_work, stats=sg.basicstats())


@app.route(URLPREFIX + "/chart")
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

    return render_template(
        "chart.html",
        bar_x=bar_x,
        bar_y=bar_y,
        stats=sg.basicstats(),
    )


@app.route(URLPREFIX + "/scatter")
def scatter():
    use_filter(request.args)
    global sg
    # scatterplot
    scat_x = []
    scat_y = []
    scat_text = []
    for a in sg.activities_work:
        scat_x.append(a.distance)
        scat_y.append(a.tempo)

        scat_text.append(a.date.strftime("%m/%d/%Y") + " id:" + a.stravaid)

    return render_template(
        "scatter.html",
        scat_x=scat_x,
        scat_y=scat_y,
        scat_text=scat_text,
        stats=sg.basicstats(),
    )


@app.route(URLPREFIX + "/chartwa")
def chartwa():
    use_filter(request.args)
    global sg
    # bar hcart by weeks
    bar_x = []
    bar_y = []
    weeklystats = sg.weeklystats()
    for week in weeklystats:
        bar_x.append("w" + week)
        bar_y.append(weeklystats[week]["distance_sum_wa"])

    return render_template(
        "chart.html",
        bar_x=bar_x,
        bar_y=bar_y,
        stats=sg.basicstats(),
    )


if __name__ == "__main__":

    app.run()
