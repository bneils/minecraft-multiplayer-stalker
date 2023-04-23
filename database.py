# This module keeps track of server history and issues out SQL commands

import sqlite3

def add_row(database_file: str, timestamp: int, online_players: list):
    con = sqlite3.connect(database_file)
    cur = con.cursor()

    # Ensure the tables exist
    cur.execute("""CREATE TABLE IF NOT EXISTS scans(
        timestamp INT,
        joined_uuids JSON DEFAULT('[]'),
        left_uuids JSON DEFAULT('[]'),
        number_online INT);""")

    cur.execute("CREATE TABLE IF NOT EXISTS online(current JSON DEFAULT('[]'));")
    res = cur.execute("SELECT current FROM online LIMIT 1;")
    row = cur.fetchone()
    online_uuids = [player.id for player in online_players]
    if row is not None:
        last_online_uuids = eval(row[0])
        last_uuids_set = set(last_online_uuids)
        now_uuids_set = set(online_uuids)
        left = list(last_uuids_set - now_uuids_set)
        joined = list(now_uuids_set - last_uuids_set)
        cur.execute("UPDATE online SET current = ?;", (repr(online_uuids),))
    else:
        left = []
        joined = online_uuids
        cur.execute("INSERT INTO online(current) VALUES (?);", (repr(online_uuids),))

    # Update UUIDs table
    cur.execute("CREATE TABLE IF NOT EXISTS uuids(uuid TEXT, username TEXT);")
    res = cur.execute("SELECT * FROM uuids;")
    uuids = {uuid:username for uuid, username in res.fetchall()}
    for player in online_players:
        if player.id not in uuids:
            cur.execute("INSERT INTO uuids(uuid, username) VALUES (?, ?);", (player.id, player.name))
        elif uuids[player.id] != player.name:
            cur.execute("UPDATE uuids SET username = ? WHERE uuid = ? LIMIT = 1", player.name, player.id)

    # To save space, a row is only written if something has changed
    if not left and not joined:
        return

    # Insert a new row, keeping mark of timestamp
    cur.execute("INSERT INTO scans(timestamp,joined_uuids,left_uuids,number_online) VALUES (?,?,?,?);",
            (timestamp, repr(joined), repr(left), len(online_players)))

    con.commit()
    con.close()

