
# This module acts as the accountant to oneshot.py
# Oneshot.py reports to the librarian about records they are checking out (leaving players).
# And books it is returning (joining players).
# The module therefore must keep track of the library's inventory, as in when records are checked in and out.
#
# record.json
#   "online" -> uuids
#   "counts" -> { timestamp -> num }
#   "log" -> { timestamp -> +/-uuid], ... }
#   "uuid" -> { uuid -> userName }

import json

class OnlinePlayerRecord:
    def __init__(self, record_file_path: str):
        self.record_file_path = record_file_path

        try:
            with open(record_file_path, "r") as record_file:
                self.record = json.load(record_file)
        except FileNotFoundError:
            self.record = {"online": [], "counts": {}, "log": [], "uuid": {}}

    def add_record(self, timestamp: int, playerObjects):
        online_uuids = set()
        for player in playerObjects:
            name = player.name
            uuid = player.id
            # Maintain uuid.dat
            if uuid not in self.record["uuid"] or self.record["uuid"][uuid] != name:
                self.record["uuid"][uuid] = name
            online_uuids.add(uuid)
        
        # self.uuids = A, B, C, D, E
        # to
        # uuids = B, C, E, F
        # who joined, who left?

        left = set(self.record["online"]) - online_uuids
        joined = online_uuids - set(self.record["online"])
        # Update log.dat
        for uuid in left:
            self.record["log"].append([timestamp, "-", uuid])
        for uuid in joined:
            self.record["log"].append([timestamp, "+", uuid])

        # Update online.dat for next time
        self.record["online"] = list(online_uuids)
        self.record["counts"][timestamp] = len(playerObjects)

    def write(self):
        with open(self.record_file_path, "w") as record_file:
            json.dump(self.record, record_file)
