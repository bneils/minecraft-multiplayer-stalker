#!/usr/bin/env python3
from mcstatus import JavaServer
from database import add_row
from datetime import datetime
from time import sleep
from socket import gaierror
import sys

maxtries = 8

server_name = sys.argv[1]
server = JavaServer.lookup(server_name)
while True:
    timestamp = int(datetime.timestamp(datetime.now()))

    for i in range(maxtries):
        try:
            status = server.status()
            players = status.players.sample
            break
        except gaierror:
            server = JavaServer.lookup(server_name)
    else:
        print("Failed after %d getaddrinfo() errors. Assuming server is down")
        players = []

    add_row(server_name + ".db", timestamp, players)

    # Adaptive waits depending on the current likelihood that any
    # one player will get up and leave (or vice versa)
    num_online = len(players)
    if 0 <= num_online <= 1:
        delay = 15
    elif 2 <= num_online <= 4:
        delay = 10
    else:
        delay = 5
    sleep(delay)
