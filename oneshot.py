#!/usr/bin/env python3
from mcstatus import JavaServer
from database import add_row
from datetime import datetime

def record_ping(server):
    timestamp = int(datetime.timestamp(datetime.now()))
    status = server.status()
    player_uuids = [player.id for player in status.players.sample]
    add_row("activity_monitor.db", timestamp, player_uuids)

server = JavaServer.lookup("kibinibottom.minecra.fr")

# server.players.online (#)
# status.latency (ms)
# status.players.sample -> [.name/.id, ...]

record_ping(server)
