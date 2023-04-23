#!/usr/bin/env python3
from mcstatus import JavaServer
from database import add_row
from datetime import datetime

server = JavaServer.lookup("kibinibottom.minecra.fr")
timestamp = int(datetime.timestamp(datetime.now()))
status = server.status()
add_row("activity_monitor.db", timestamp, status.players.sample)
print(len(status.players.sample))
