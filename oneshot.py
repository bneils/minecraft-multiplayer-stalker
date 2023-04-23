#!/usr/bin/env python3
from mcstatus import JavaServer
from database import add_row
from datetime import datetime

def record_ping(server):
    timestamp = int(datetime.timestamp(datetime.now()))
    status = server.status()
    add_row("activity_monitor.db", timestamp, status.players.sample)

server = JavaServer.lookup("kibinibottom.minecra.fr")

# server.players.online (#)
# status.latency (ms)
# status.players.sample -> [.name/.id, ...]

record_ping(server)
