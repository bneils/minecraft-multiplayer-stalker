#!/usr/bin/env python3
import sqlite3
import sys
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

server_file = sys.argv[1]

# Print individual intervals that each player was online, as well as the duration of the session
try:
    con = sqlite3.connect(f"file:{server_file}?mode=ro", uri=True)
except sqlite3.OperationalError:
    print("That db file doesn't exist")
    exit()
cur = con.cursor()

res = cur.execute("SELECT * FROM scans")
rows = []
for row in res.fetchall():
    timestamp, joined_uuids, left_uuids, number_online = row
    rows.append((timestamp, eval(joined_uuids), eval(left_uuids), number_online))

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
for row in rows:
    print(datetime.fromtimestamp(row[0]).strftime(date_format), row[3])
