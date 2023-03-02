#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Last Modified: 2022/11/29 14:42:58
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
    elapsed_time: float
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
                stravaid=str(activity["id"]),
                start_date_local=activity["start_date_local"],
                name=activity["name"],
                distance=round(activity["distance"] / 1000, 2),  # til km
                moving_time=activity["moving_time"],  # sekunder
                elapsed_time=activity["elapsed_time"],  # sekumder
                average_speed=activity["average_speed"],  # m/s (ikek checket)
                sport_type=activity["sport_type"],
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

    def weeklystats(self):
        # dan listen af uger så der er plads til uger uden løb

        date_firstrun = self.basicstats()["runs"]["first_run"].date
        monday = date_firstrun - timedelta(days=date_firstrun.weekday())
        date_lastrun = self.basicstats()["runs"]["last_run"].date
        stats = {}
        weekcount = 0
        while monday <= date_lastrun:
            week = (
                str(monday.isocalendar().year)
                + "."
                + str(monday.isocalendar().week).zfill(2)
            )
            stats[week] = {
                "distance_sum": 0,
                "distance_sum_wa": 0,
                "distance_max": 0,
                "numberruns": 0,
                "monday": monday,
                "weekcount": weekcount,
            }
            monday = monday + timedelta(days=7)
            weekcount = weekcount + 1

        # beregner sum, antal og max af aktivitter pr uge
        for a in self.activities_work:
            stats[a.week]["distance_sum"] = stats[a.week]["distance_sum"] + a.distance
            stats[a.week]["numberruns"] = stats[a.week]["numberruns"] + 1
            stats[a.week]["distance_max"] = max(
                stats[a.week]["distance_max"], a.distance
            )

        # beregn vægtet løbende gennemsnit.

        keys = list(stats.keys())  # liste af ugenumre på formen 2022.31
        for i in range(len(keys)):
            data0 = stats[keys[i]]  # indeværende uge
            if i == 0:
                dataBefore = stats[keys[i]]  # ved første uge brug indeværende uge
                dataAfter = stats[keys[i + 1]]
            elif i == len(keys) - 1:
                dataBefore = stats[keys[i - 1]]
                dataAfter = stats[keys[i]]  # ved sidste uge brug indeværende uge
            else:
                dataBefore = stats[keys[i - 1]]
                dataAfter = stats[keys[i + 1]]
            distance_sum_wa = (
                dataBefore["distance_sum"]
                + data0["distance_sum"] * 3
                + dataAfter["distance_sum"]
            ) / 5
            data0["distance_sum_wa"] = round(distance_sum_wa, 2)

        return stats

    def linear_regression(self):
        weekdata = self.weeklystats()
        x = []
        y = []
        for w in weekdata:
            x.append(weekdata[w]["weekcount"])
            y.append(weekdata[w]["distance_sum"])

        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum([xi * yi for xi, yi in zip(x, y)])
        sum_xx = sum([xi**2 for xi in x])

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
        intercept = (sum_y - slope * sum_x) / n

        # residuals = [yi - (slope * xi + intercept) for xi, yi in zip(x, y)]
        # ss_res = sum([residual**2 for residual in residuals])
        # ss_tot = sum([(yi - sum_y / n) ** 2 for yi in y])
        # r_squared = 1 - (ss_res / ss_tot)

        return slope, intercept


if __name__ == "__main__":
    client = stravaClient()
    client.refresh_token = conf["STRAVA"]["refresh_token"]  # til test
    client.getToken()
    statsgenerator = StatsGenerator(client.runningactivities())
    print(len(statsgenerator.activities_work))
    # statsgenerator.filter(lambda a: a.distance > 1)
    statsgenerator.filter(lambda a: a.date >= date(2023, 1, 1))
    # statsgenerator.sort(lambda a: -a.distance)
    print(f"Antal aktiviteter i work: {len(statsgenerator.activities_work)}")
    # pp(statsgenerator.activities_work)

    print(statsgenerator.basicstats())
    print(statsgenerator.activities_work[0].week)
    print(statsgenerator.weeklystats())
    print(statsgenerator.linear_regression())
