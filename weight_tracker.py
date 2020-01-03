#!/usr/bin/python3
import sqlite3
from typing import List, Tuple
import argparse

class WeightTracker():
    def __init__(self, db_name: str="weight_tracker.db"):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS weight_logs(
                date TEXT UNIQUE,
                weight INTEGER
                )""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS user_data(
                name TEXT,
                start_weight INTEGER,
                goal_weight INTEGER,
                start_date TEXT,
                goal_date TEXT
                )""")
        self.conn.commit()

    def insert_weight(self, weight: int, date: str="") -> None:
        sql = """
                INSERT INTO weight_logs(weight, date)
                VALUES(?, {})
                """
        sql_update = """
            UPDATE weight_logs
            SET weight=?
            WHERE date={}
        """
        curr_date = "strftime('%Y-%m-%d','now')"
        if date is "":
            sql = sql.format(curr_date)
            sql_update = sql_update.format(curr_date)
            params = [weight]
        else:
            sql = sql.format("?")
            sql_update = sql_update.format("?")
            params = [weight, date]
        try:
            self.cur.execute(sql, params)
            self.conn.commit()
        except:
            self.cur.execute(sql_update, params)
            self.conn.commit()

    def get_weight(self, date: str) -> int:
        sql = """
                SELECT weight
                FROM weight_logs
                WHERE date=?
                """
        self.cur.execute(sql, [date])
        self.conn.commit()
        try:
            return self.cur.fetchone()[0]
        except:
            return 0

    def get_weight_logs(self) -> List[Tuple[str, int]]:
        self.cur.execute("SELECT * FROM weight_logs")
        self.conn.commit()
        return self.cur.fetchall()

if "__main__" in __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--insert")
    parser.add_argument("-db", "--db_name")
    parser.add_argument("-d", "--date")
    args = parser.parse_args()
    if args.db_name:
        wt = WeightTracker(args.db_name)
    else:
        wt = WeightTracker()
    if args.insert:
        if args.date:
            wt.insert_weight(int(args.insert), args.date)
        else:        
            wt.insert_weight(int(args.insert))
    print("*****weight logs**** {}".format(wt.get_weight_logs()))
