#!/usr/bin/env python3
from mcstatus import JavaServer
from librarian import OnlinePlayerRecord
from datetime import datetime

print("Looking up server")
server = JavaServer.lookup("kibinibottom.minecra.fr")

print("Looking up status")
status = server.status()

# server.players.online (#)
# status.latency (ms)
# status.players.sample -> [.name/.id, ...]

record = OnlinePlayerRecord("log.dat", "online.dat", "uuid.dat")
record.add_record(int(datetime.timestamp(datetime.now())), status.players.sample)

record.write()
