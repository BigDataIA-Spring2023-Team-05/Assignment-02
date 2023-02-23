import unittest
import pandas as pd
import re
from utils.logger import Log as log
import sqlite3 as sql
from utils.logger import Log
import os
from pathlib import Path
import json

class MapData:
    
    def __init__(self) -> None:
        self.database_name = 'assignment_2.db'
        self.table_name = 'MapData'
        self.create_query = f'Create table if not Exists {self.table_name} (Name,County,Lat,Lon,Elev)'


        self.database_file_path = os.path.join(os.path.dirname(__file__), self.database_name)

        self.is_database_initilization()
        self.load_data()



    def create_database(self):
        db = sql.connect(self.database_file_path, check_same_thread=False)
        cursor = db.cursor()
        cursor.executescript(self.create_query)
        db.commit()
        db.close()
        log().i('Database initialized succesfully!')


    def is_database_initilization(self):
        if not Path(self.database_file_path).is_file():
            log().i('Database file not found, initilizing...')
            self.create_database()
        else:
            log().i('Database file already exist')
    
    def db_open_connection(self):
        self.conn = sql.connect(self.database_file_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def db_close_connection(self):
        self.conn.commit()        
        if (self.conn):
            self.conn.close()
            log().i('The SQLite connection is closed')
        else:
            log().i('The SQLite connection is already closed')


    def load_data(self):
        data = pd.read_fwf('https://www.ncei.noaa.gov/access/homr/file/nexrad-stations.txt', nrows=100000)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data = data.drop(index = 0,axis = 0)

        self.db_open_connection()
        
        df = pd.DataFrame()
        df['name']=data['name']
        df['county']=data['county']
        df['lat'] = data['lat']
        df['lon'] = data['lon']
        df['elev'] = data['elev']

        df.to_sql(self.table_name, self.conn, if_exists='replace', index=False)
        
        self.db_close_connection()

    def get_data_for_map(self):
        self.db_open_connection()

        # data = self.cursor.executescript("SELECT * from Mapdata")

        self.cursor.execute("SELECT * FROM Mapdata")
        row_headers=[x[0] for x in self.cursor.description] #this will extract row headers

        myresult = self.cursor.fetchall()

        json_data=[]
        for result in myresult:
                json_data.append(dict(zip(row_headers, result)))
        return json_data
    
        # self.conn.commit()

        # df = pd.read_sql_query("SELECT * from Mapdata", self.conn)

        # self.db_close_connection()

        return myresult


