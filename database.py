
# This module keeps track of server history

import sqlite3

def add_row(database_file: str, timestamp: int, online_uuids: list):
    con = sqlite3.connect(database_file)
    cur = con.cursor()
    con.row_factory = sqlite3.Row

    # Ensure the tables exist
    cur.execute("""CREATE TABLE IF NOT EXISTS scans(
        timestamp INT,
        joined_uuids JSON DEFAULT('[]'),
        left_uuids JSON DEFAULT('[]'),
        online_uuids JSON DEFAULT('[]'));""")

    # Get the last row, compare changes
    res = cur.execute("SELECT * FROM scans ORDER BY timestamp DESC LIMIT 1;")
    row = cur.fetchone()
    if row is not None:
        last_online_uuids = eval(row[-1])
        last_uuids_set = set(last_online_uuids)
        now_uuids_set = set(online_uuids)
        left = list(last_uuids_set - now_uuids_set)
        joined = list(now_uuids_set - last_uuids_set)
    else:
        left = []
        joined = online_uuids

    # To save space, a row is only written if something has changed
    if not left and not joined:
        return

    # Insert a new row, keeping mark of timestamp
    cur.execute("INSERT INTO scans(timestamp,joined_uuids,left_uuids,online_uuids) VALUES (?,?,?,?);",
            (timestamp, repr(joined), repr(left), repr(online_uuids)))

    con.commit()
    con.close()

