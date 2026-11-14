#!/usr/bin/env python3
"""Decide whether a run has anything left to update. Exit 0 = settled, skip the run. Exit 1 = run.

The skins day is settled only when all three of these agree:
  1. ESPN lists at least one game for the skins date and every one of them is final.
  2. skins_history/<date>.csv holds a result for exactly those teams, with the same winners and scores.
  3. The published page was built during this skins day and shows exactly those games, all final,
     with the same scores.

Anything else exits 1 and the run goes ahead as usual: a game still to play, a missing or different
score, a game missing from the file, a page from an earlier day, a site that can't be reached, or a
format this script doesn't recognise. So a mistake here can only cost an unnecessary run.

The skins sites (SportsLine, Gambletron, plaintextsports) are never contacted from here: one request
goes to ESPN's scoreboard API and one to our own GitHub Pages site.
"""
import csv
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

CENTRAL = ZoneInfo("America/Chicago")
# ESPN abbreviation -> ours (same list as espn_links() in skins_today.qmd)
ESPN_FIX = {"GS": "GSW", "NY": "NYK", "SA": "SAS", "NO": "NOP", "UTAH": "UTA", "WSH": "WAS"}


class NotSettled(Exception):
    pass


def skins_date(now):
    """A skins day runs 2 AM - 2 AM Central (same rule as skins_today.qmd)."""
    return (now.astimezone(CENTRAL) - timedelta(hours=2)).date()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (skins-gate)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")


def read_source(env_file, url):
    """Test hook: a local file named in the environment replaces the request."""
    path = os.environ.get(env_file)
    if path:
        with open(path, encoding="utf-8") as f:
            return f.read()
    return fetch(url)


def espn_finals(day):
    """{team: (own score, opponent score)} for the day, or NotSettled unless every game is final."""
    text = read_source("SKINS_ESPN_FILE", "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates="
                       + day.strftime("%Y%m%d"))
    events = json.loads(text).get("events", [])
    if not events:
        raise NotSettled("ESPN lists no games for " + str(day))
    finals = {}
    for ev in events:
        comp = ev["competitions"][0]
        status = comp.get("status", ev.get("status", {})).get("type", {})
        if status.get("name") != "STATUS_FINAL" or not status.get("completed"):
            raise NotSettled(ev.get("shortName", "a game") + " is not final (" + str(status.get("name")) + ")")
        teams = [(ESPN_FIX.get(c["team"]["abbreviation"], c["team"]["abbreviation"]), int(c["score"])) for c in comp["competitors"]]
        if len(teams) != 2 or teams[0][1] == teams[1][1]:
            raise NotSettled("unexpected ESPN result for " + ev.get("shortName", "a game"))
        for (team, own), (_, opp) in (teams, teams[::-1]):
            if team in finals:
                raise NotSettled(team + " appears twice on ESPN's scoreboard")
            finals[team] = (own, opp)
    return finals


def check_history(day, finals, history_dir):
    path = os.path.join(history_dir, str(day) + ".csv")
    if not os.path.exists(path):
        raise NotSettled("no history file for " + str(day))
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    teams = [r.get("Abbr", "") for r in rows]
    if sorted(teams) != sorted(finals):
        raise NotSettled("history file teams differ from ESPN's games: file has %d, ESPN has %d" % (len(teams), len(finals)))
    for r in rows:
        own, opp = finals[r["Abbr"]]
        if r.get("Won_Game") not in ("TRUE", "FALSE"):
            raise NotSettled("history file has no result yet for " + r["Abbr"])
        if (r["Won_Game"] == "TRUE") != (own > opp):
            raise NotSettled("history file has a different winner than ESPN for " + r["Abbr"])
        if r.get("Final_Score") != "%d-%d" % (own, opp):
            raise NotSettled("history file score for %s is %s, ESPN has %d-%d" % (r["Abbr"], r.get("Final_Score"), own, opp))


def check_page(day, finals, now):
    repo = os.environ.get("GITHUB_REPOSITORY", "ejperez2/Daily-Skins-Matchups")
    owner, name = repo.split("/", 1)
    # The query string only keeps a CDN from handing back an older copy
    html = read_source("SKINS_PAGE_FILE", "https://%s.github.io/%s/?gate=%d" % (owner, name, int(now.timestamp())))
    built = re.search(r"""data-built=["'](\d+)["']""", html)
    if not built:
        raise NotSettled("published page has no build time")
    built_day = skins_date(datetime.fromtimestamp(int(built.group(1)), CENTRAL))
    if built_day != day:
        raise NotSettled("published page is from " + str(built_day))
    start = re.search(r"""id=["']sk-today-games["']""", html)
    end = re.search(r"""id=["']fold-(?:odds|yesterday)["']""", html)  # whichever section follows the games
    if not start or not end or end.start() < start.end():
        raise NotSettled("published page has no games section")
    games = html[start.end():end.start()]
    states = re.findall(r"""<article\b[^>]*\bdata-state=["']([a-z]+)["']""", games)
    if len(states) * 2 != len(finals) or any(s != "final" for s in states):
        raise NotSettled("published page shows %d games, %d of them final; ESPN has %d" % (len(states), states.count("final"), len(finals) // 2))
    sides = re.findall(r"""<div class=["']abbr["']>([A-Z]{2,4})</div>.*?<div class=["']score["']>(\d*)</div>""", games, re.S)
    shown = dict(sides)
    if len(sides) != len(finals) or sorted(shown) != sorted(finals):
        raise NotSettled("published page teams differ from ESPN's games")
    for team, (own, _) in finals.items():
        if shown[team] != str(own):
            raise NotSettled("published page score for %s is %s, ESPN has %d" % (team, shown[team] or "blank", own))


def main():
    now = datetime.fromisoformat(os.environ["SKINS_NOW"]) if os.environ.get("SKINS_NOW") else datetime.now(CENTRAL)
    day = skins_date(now)
    try:
        finals = espn_finals(day)
        check_history(day, finals, os.environ.get("SKINS_HISTORY_DIR", "skins_history"))
        check_page(day, finals, now)
    except NotSettled as why:
        print("Not settled for %s: %s. Running." % (day, why))
        return 1
    except Exception as err:  # unreachable site, unexpected format, anything else: run as usual
        print("Could not tell whether %s is settled (%s: %s). Running." % (day, type(err).__name__, err))
        return 1
    print("Settled for %s: all %d games are final, saved and published. Nothing to update." % (day, len(finals) // 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
