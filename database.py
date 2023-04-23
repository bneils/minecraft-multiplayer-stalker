
# This module keeps track of server history

import sqlite3

def add_row(database_file: str, timestamp: int, online_uuids: list):
    con = sqlite3.connect(database_file)
    cur = con.cursor()

    # Ensure the tables exist
    cur.execute("""CREATE TABLE IF NOT EXISTS scans(
        timestamp INT,
        joined_uuids JSON DEFAULT('[]'),
        left_uuids JSON DEFAULT('[]'));""")

    cur.execute("CREATE TABLE IF NOT EXISTS online(current JSON DEFAULT('[]'));")
    res = cur.execute("SELECT current FROM online LIMIT 1;")
    row = cur.fetchone()
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

    # To save space, a row is only written if something has changed
    if not left and not joined:
        return

    # Insert a new row, keeping mark of timestamp
    cur.execute("INSERT INTO scans(timestamp,joined_uuids,left_uuids) VALUES (?,?,?);",
            (timestamp, repr(joined), repr(left)))

    con.commit()
    con.close()

