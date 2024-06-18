import sqlite3
from datetime import datetime
import pandas as pd


class DataAnalyzer:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def fetch_data(self):
        query = "SELECT name, wait_time, last_updated FROM rides"
        df = pd.read_sql_query(query, self.conn)
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        return df

    def average_wait_time(self):
        query = "SELECT AVG(wait_time) FROM rides WHERE is_open = 1"
        avg_wait_time = self.fetch_data(query)[0][0]
        return avg_wait_time

    def busiest_ride(self):
        query = """
        SELECT name, AVG(wait_time) as avg_wait
        FROM rides
        WHERE is_open = 1
        GROUP BY name
        ORDER BY avg_wait DESC
        LIMIT 1
        """
        busiest_ride = self.fetch_data(query)[0]
        return busiest_ride

    def wait_time_trends(self):
        df = self.fetch_data()
        df['wait_tme'] = pd.to_numeric(df['wait_time'], errors='coerce')
        df['wait_time'].fillna(0,inplace=True)
        trends = df.groupby('name').resample('D', on='last_updated')['wait_time'].mean(numneric_only=True).reset_index()
        return trends
