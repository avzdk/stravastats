#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Last Modified: 2022/11/10 12:05:34
from dataclasses import dataclass
from strava import Strava
from datetime import datetime, date, timedelta
from pprint import pp
import logging
import configparser
import os

ENVIRONMENT = os.environ.get("ENV", "local")
print(f"env:{ENVIRONMENT}")
conf = configparser.ConfigParser()
if ENVIRONMENT == "local":
    cf = conf.read(os.path.join(os.path.dirname(__file__), "config_local.ini"))
else:
    cf = conf.read(os.path.join(os.path.dirname(__file__), "config.ini"))

log = logging.getLogger(__name__)

log = logging.getLogger(__name__)

log.info("Start")


@dataclass
class Activity:
    stravaid: str
    start_date_local: str
    name: str
    distance: float  # meter
    moving_time: float
    average_speed: float
    sport_type: str
    # date : datetime = None

    @property
    def tempo(self):  # minutter
        return 1 / self.average_speed * 1000 / 60

    @property
    def date(self):
        return datetime.strptime(self.start_date_local[0:10], "%Y-%m-%d").date()

    @property
    def week(self):  # 2022.42
        return (
            str(self.date.isocalendar().year)
            + "."
            + str(self.date.isocalendar().week).zfill(2)
        )

    @property
    def tempo_in_txt(self):
        return str(timedelta(minutes=self.tempo))[2:7]

    @property
    def stravaurl(self):
        return "https://www.strava.com/activities/" + self.stravaid

    def __repr__(self):
        return f"Activity({self.date}  {self.distance/1000:.2f} km   {self.name}  {self.moving_time/60:.2f} min. Tempo:{self.tempo:.2f})\n"


class stravaClient(Strava):
    def runningactivities(self, after_date: date = date(1974, 1, 1)):
        # henter alle aktiviteter ved at kalde API flere gange indtil der ikke er flere.
        # filtrerer desuden så det kun er løb.
        # self.getToken()
        activities_raw = []
        for page in range(1, 500):
            rv = self.getActivities(
                200, page, datetime.combine(after_date, datetime.min.time())
            )
            if rv != []:
                activities_raw = activities_raw + rv
            else:
                break
        log.info(f"ANTAL {len(activities_raw)} hentet")
        activities_raw = list(
            filter(lambda a: a["sport_type"] == "Run", activities_raw)
        )
        log.info(f"heraf {len(activities_raw)} løb")
        activities_raw = list(filter(lambda a: a["distance"] > 1, activities_raw))
        log.info(f"efter fjernelse af dist=0 : {len(activities_raw)} ")

        activities: list[Activity] = []  # samtlige aktiviteter.
        for activity in activities_raw:
            dc = Activity(
                str(activity["id"]),
                activity["start_date_local"],
                activity["name"],
                round(activity["distance"] / 1000, 2),
                activity["moving_time"],
                activity["average_speed"],
                activity["sport_type"],
            )
            activities.append(dc)

        return activities


class StatsGenerator:
    def __init__(self, activities_main):
        self.activities_main = activities_main
        self.reset()

    def reset(self):
        # vender tilbage til den samlede liste af løb.
        self.activities_work = self.activities_main.copy()

    def filter(self, filterfunction):
        # filtrerer og overskriver activities_work
        # Eksempel på anvendelse statsgenerator.filter(lambda a: a.distance > 15000)
        self.activities_work = list(filter(filterfunction, self.activities_work))

    def sort(self, sortfunction):
        # sorterer og overskriver activities_work
        # Eksempel på anvendelse statsgenerator.sort(lambda a: -a.distance)
        self.activities_work = list(sorted(self.activities_work, key=sortfunction))

    def basicstats(self):

        stats = {}
        stats["runs"] = {}
        stats["runs"]["distance_max"] = max(
            self.activities_work, key=lambda a: a.distance
        )
        stats["runs"]["distance_min"] = min(
            self.activities_work, key=lambda a: a.distance
        )
        stats["runs"]["tempo_max"] = max(self.activities_work, key=lambda a: a.tempo)
        stats["runs"]["tempo_min"] = min(self.activities_work, key=lambda a: a.tempo)
        stats["runs"]["first_run"] = min(self.activities_work, key=lambda a: a.date)
        stats["runs"]["last_run"] = max(self.activities_work, key=lambda a: a.date)

        stats["totals"] = {
            "days": abs(
                stats["runs"]["last_run"].date - stats["runs"]["first_run"].date
            ).days,
            "number_runs": len(self.activities_work),
            "total_distance": round(sum(a.distance for a in self.activities_work), 2),
        }

        return stats


if __name__ == "__main__":
    client = stravaClient()
    client.refresh_token = conf["STRAVA"]["refresh_token"]  # til test
    client.getToken()
    statsgenerator = StatsGenerator(client.runningactivities())
    print(len(statsgenerator.activities_work))
    statsgenerator.filter(lambda a: a.distance > 1)
    statsgenerator.filter(lambda a: a.date > date(2022, 1, 1))
    statsgenerator.sort(lambda a: -a.distance)
    print(len(statsgenerator.activities_work))
    pp(statsgenerator.activities_work)

    print(statsgenerator.basicstats())
    print(statsgenerator.activities_work[0].week)
