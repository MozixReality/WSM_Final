import os
import csv
from datetime import datetime
from itertools import islice

DATA_PATH = "./Data"
SESSIONS_FILE = "train_sessions.csv"
PURCHASES_FILE = "train_purchases.csv"

class Session:
    def __init__(self, id, item, time):
        self.id = id
        self.items = [item]
        try:
            self.start_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
            self.end_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        except:
            self.start_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            self.end_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    def add_items(self, item, time):
        self.items.append(item)
        try:
            new_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        except:
            new_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        self.start_time = min(self.start_time, new_time)
        self.end_time = max(self.end_time, new_time)

    def add_purchased_item(self, item, time):
        self.purchased_item = item
        try:
            new_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        except:
            new_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        self.perchase_time = new_time

    def viewed_items(self):
        return self.items

    def total_viewing_time(self):
        return self.end_time - self.start_time

    def purchased_info(self):
        return self.purchased_item, self.perchase_time

Sessions = []
with open(os.path.join(DATA_PATH, SESSIONS_FILE)) as csvfile:
    rows = csv.reader(csvfile)
    session_id, start_time = None, None
    for row in islice(rows, 1, None):
        cur_session_id, item, time = row[0], row[1], row[2]
        if session_id != cur_session_id:
            session_id, start_time = cur_session_id, time
            Sessions.append(Session(session_id, item, start_time))
        else:
            Sessions[-1].add_items(item, time)

print("OK")
session_index = 0
with open(os.path.join(DATA_PATH, PURCHASES_FILE)) as csvfile:
    rows = csv.reader(csvfile)
    for row in islice(rows, 1, None):
        session_id, purchase_item, time = row[0], row[1], row[2]
        if Sessions[session_index].id == session_id:
            Sessions[session_index].add_purchased_item(purchase_item, time)
        else:
            print(session_id)
            exit()

        session_index += 1

print("OK")
a, b = Sessions[-1].purchased_info()
print(a, b)
