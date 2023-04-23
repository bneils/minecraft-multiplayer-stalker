#!/usr/bin/env python3
import sqlite3
from datetime import datetime

def secs_to_humanreadable(s):
    days = int(s / (60 * 60 * 24))
    hours = int(s / (60 * 60) % 24)
    minutes = int(s / 60 % 60)
    seconds = int(s % 60)

    msg = []
    if days:
        msg.append("%d days" % days)
    if hours:
        msg.append("%d hours" % hours)
    if minutes:
        msg.append("%d mins" % minutes)
    if seconds:
        msg.append("%d secs" % seconds)
    return ", ".join(msg)

# Print individual intervals that each player was online, as well as the duration of the session
con = sqlite3.connect("activity_monitor.db")
cur = con.cursor()

res = cur.execute("SELECT * FROM scans")
rows = []
for row in res.fetchall():
    timestamp, joined_uuids, left_uuids = row
    rows.append((timestamp, eval(joined_uuids), eval(left_uuids)))

res = cur.execute("SELECT * FROM uuids")
uuids = {uuid:username for uuid, username in res.fetchall()}

date_format = "%m/%d %I:%M:%S %p"

for i in range(len(rows)):
    start = rows[i][0]
    for joined_player in rows[i][1]:
        username = uuids.get(joined_player, joined_player).ljust(16, " ")
        for j in range(i + 1, len(rows)):
            if joined_player in rows[j][2]:
                end = rows[j][0]
                duration = end - start
                msg = "%s was online from %s to %s (%s)" % (username, datetime.fromtimestamp(start).strftime(date_format),
                        datetime.fromtimestamp(end).strftime(date_format), secs_to_humanreadable(duration))
                print(msg)
                break
        else:
            duration = datetime.timestamp(datetime.now()) - start
            msg = "%s has been online since %s" % (username, datetime.fromtimestamp(start).strftime(date_format))
            print(msg.ljust(72, " ") + "(%s)" % secs_to_humanreadable(duration))

# Display number of people online, every time it changes, and what time it was
