#!/usr/bin/python3
import sqlite3
from typing import List, Tuple, Any
import argparse

class WeightTracker():
    def __init__(self, name, **kwargs):
        self.db_name = "weight_tracker.db"
        if 'db_name' in kwargs and kwargs['db_name']:
            self.db_name = kwargs['db_name']
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS weight_logs(
                date TEXT UNIQUE,
                weight INTEGER
                )""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS user_data(
                name TEXT UNIQUE,
                start_weight INTEGER,
                goal_weight INTEGER,
                start_date TEXT,
                goal_date TEXT
                )""")
        self.conn.commit()
        user_info = self.get_user_info(name)
        if user_info is None:
            sql = """INSERT INTO 
                user_data(name, start_weight, goal_weight, start_date, goal_date)
                VALUES(?,?,?,?,?)"""
            self.cur.execute(sql, [name, kwargs['start_weight'], kwargs['goal_weight'],
                kwargs['start_date'], kwargs['goal_date']])
            self.conn.commit()
            self.user_info = {
                    "name": name,
                    "start_weight": kwargs['start_weight'],
                    "goal_weight": kwargs['goal_weight'],
                    "start_date": kwargs['start_date'],
                    "goal_date": kwargs['goal_date']
                    }
        else:
            self.user_info = {
                    "name": name,
                    "start_weight": user_info[1],
                    "goal_weight": user_info[2],
                    "start_date": user_info[3],
                    "goal_date": user_info[4]
                    }
            keys = ['start_weight', 'goal_weight', 'start_date', 'goal_date']
            for key in keys:
                value = kwargs.get(key)
                if value:
                    self.user_info[key] = value
            self._update_user_info()

    def get_user_info(self, name: str) -> Tuple:
        sql = "SELECT * FROM user_data WHERE name=?"
        self.cur.execute(sql, [name])
        return self.cur.fetchone()

    def _update_user_info(self) -> None:
        user_info = [
                self.user_info["start_weight"],
                self.user_info["goal_weight"],
                self.user_info["start_date"],
                self.user_info["goal_date"],
                self.user_info["name"]
                ]
        sql = """UPDATE user_data
            SET start_weight=?,
                goal_weight=?,
                start_date=?,
                goal_date=?
            WHERE name=?
        """
        self.cur.execute(sql, user_info)
        self.conn.commit()

    def insert_weight(self, weight: int, date: str=None) -> None:
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
        params: List[Any] = []
        if date is None:
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
        try:
            return self.cur.fetchone()[0]
        except:
            return 0

    def get_latest_weight(self) -> Tuple[int, str]:
        self.cur.execute("""
            SELECT weight, MAX(date)
            FROM weight_logs""")
        return self.cur.fetchone()

    def get_weight_logs(self) -> List[Tuple[str, int]]:
        self.cur.execute("SELECT * FROM weight_logs")
        return self.cur.fetchall()

if "__main__" in __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--insert_weight")
    parser.add_argument("-db", "--db_name")
    parser.add_argument("-n", "--name")
    parser.add_argument("-d", "--date")
    parser.add_argument("-sw", "--start_weight")
    parser.add_argument("-gw", "--goal_weight")
    parser.add_argument("-sd", "--start_date")
    parser.add_argument("-gd", "--goal_date")
    args = parser.parse_args()
    wt = WeightTracker(**vars(args))
    if args.insert_weight:
        if args.date:
            wt.insert_weight(int(args.insert_weight), args.date)
        else:        
            wt.insert_weight(int(args.insert_weight))
    print("*****weight logs**** {}".format(wt.get_weight_logs()))
    print("name " +wt.user_info.get('name'))
    print("start weight {}".format(wt.user_info.get("start_weight")))
    print("goal weight {}".format(wt.user_info.get("goal_weight")))
    print("start date {}".format(wt.user_info.get("start_date")))
    print("goal date {}".format(wt.user_info.get("goal_date")))
    print("latest weight {}".format(wt.get_latest_weight()))
