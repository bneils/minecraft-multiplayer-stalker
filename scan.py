#!/usr/bin/env python3
from mcstatus import JavaServer
from database import add_row
from datetime import datetime
from time import sleep
import sys

server_name = sys.argv[1]
server = JavaServer.lookup(server_name)
while True:
    timestamp = int(datetime.timestamp(datetime.now()))
    status = server.status()
    add_row(server_name + ".db", timestamp, status.players.sample)

    # Adaptive waits depending on the current likelihood that any
    # one player will get up and leave (or vice versa)
    num_online = len(status.players.sample)
    if 0 <= num_online <= 1:
        delay = 15
    elif 2 <= num_online <= 4:
        delay = 10
    else:
        delay = 5
    
    sleep(delay)
