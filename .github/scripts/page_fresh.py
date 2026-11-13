#!/usr/bin/env python3
"""Exit 0 if the published page was built less than FRESH_MINUTES ago, 1 otherwise.

Used only for runs started by GitHub's own schedule. Updates are normally started on the 20-minute
mark by something else, and GitHub's schedule fires too, sometimes minutes after one of those. A scheduled
run that finds the page was just rebuilt has nothing to add, so it stops before scraping anything.

Exit 1 (run as usual) for anything else: an old page, a page without a build stamp, an unreachable
site. A mistake here can only cost an unnecessary run, never a missed update.
Only our own GitHub Pages site is contacted.
"""
import os
import re
import sys
import time
import urllib.request

FRESH_MINUTES = 10


def main():
    now = float(os.environ.get("SKINS_NOW_EPOCH") or time.time())
    try:
        path = os.environ.get("SKINS_PAGE_FILE")
        if path:
            html = open(path, encoding="utf-8").read()
        else:
            repo = os.environ.get("GITHUB_REPOSITORY", "ejperez2/Daily-Skins-Matchups")
            owner, name = repo.split("/", 1)
            # The query string only keeps a CDN from handing back an older copy
            req = urllib.request.Request("https://%s.github.io/%s/?fresh=%d" % (owner, name, int(now)),
                                         headers={"User-Agent": "Mozilla/5.0 (skins-gate)"})
            html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
        built = re.search(r"""data-built=["'](\d+)["']""", html)
        if not built:
            print("Published page has no build time. Running.")
            return 1
        age = (now - int(built.group(1))) / 60
    except Exception as err:
        print("Could not read the published page (%s: %s). Running." % (type(err).__name__, err))
        return 1
    if 0 <= age < FRESH_MINUTES:
        print("Published page was built %.1f minutes ago; skipping this scheduled run." % age)
        return 0
    print("Published page was built %.1f minutes ago. Running." % age)
    return 1


if __name__ == "__main__":
    sys.exit(main())
