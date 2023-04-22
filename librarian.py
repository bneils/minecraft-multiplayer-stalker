
# This module acts as the accountant to oneshot.py
# Oneshot.py reports to the librarian about records they are checking out (leaving players).
# And books it is returning (joining players).
# The module therefore must keep track of the library's inventory, as in when records are checked in and out.
#
# online.dat contains a CSV list of UUIDs of currently active players since last scanned
# log.dat contains lines in this format:
# <unixtimestamp> (+/-) <uuid>
# uuid.dat contains UUID to username mappings in the format "UUID username" for each line

class OnlinePlayerRecord:
    def __init__(self, log_file_path: str, online_file_path: str, uuid_file_path: str):
        self.log_file_path = log_file_path
        self.online_file_path = online_file_path
        self.uuid_file_path = uuid_file_path

        try:
            with open(log_file_path, "r") as log_file:
                log_lines = log_file.read().splitlines()
        except FileNotFoundError:
            log_lines = []
        self.log = []
        for line in log_lines:
            timestamp, change, uuid = line.split(" ")
            if change not in ("-", "+"):
                raise ValueError()
            self.log.append(int(timestamp), change, uuid)

        try:
            with open(online_file_path, "r") as online_file:
                self.online_uuids = set(online_file.read().split(","))
        except FileNotFoundError:
            self.online_uuids = set()

        try:
            with open(uuid_file_path, "r") as uuid_file:
                self.uuids = {}
                for line in uuid_file.read().splitlines():
                    uuid, name = line.split(" ")
                    self.uuids[uuid] = name
        except FileNotFoundError:
            self.uuids = {}

    def add_record(self, timestamp: int, playerObjects):
        online_uuids = set()
        for player in playerObjects:
            name = player.name
            uuid = player.id
            # Maintain uuid.dat
            if uuid not in self.uuids or self.uuids[uuid] != name:
                self.uuids[uuid] = name
            online_uuids.add(uuid)
        
        # self.uuids = A, B, C, D, E
        # to
        # uuids = B, C, E, F
        # who joined, who left?

        left = self.online_uuids - online_uuids
        joined = online_uuids - self.online_uuids
        # Update log.dat
        for uuid in left:
            self.log.append((timestamp, "-", uuid))
        for uuid in joined:
            self.log.append((timestamp, "+", uuid))

        # Update online.dat for next time
        self.online_uuids = online_uuids

    def write(self):
        string_builder = []
        for record in self.log:
            string_builder.append(" ".join(map(str, record)))
        with open(self.log_file_path, "w") as record_file:
            record_file.write("\n".join(string_builder))

        with open(self.online_file_path, "w") as online_file:
            online_file.write(",".join(self.online_uuids))

        string_builder.clear()
        for uuid, username in self.uuids.items():
            string_builder.append(uuid + " " + username)

        with open(self.uuid_file_path, "w") as uuid_file:
            uuid_file.write("\n".join(string_builder))
