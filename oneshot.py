#!/usr/bin/env python3
from mcstatus import JavaServer
from librarian import OnlinePlayerRecord
from datetime import datetime

def record_ping(record, server):
    timestamp = int(datetime.timestamp(datetime.now()))
    status = server.status()
    record.add_record(timestamp, status.players.sample)

server = JavaServer.lookup("kibinibottom.minecra.fr")

# server.players.online (#)
# status.latency (ms)
# status.players.sample -> [.name/.id, ...]

record = OnlinePlayerRecord("record.json")
record_ping(record, server)
record.write()
