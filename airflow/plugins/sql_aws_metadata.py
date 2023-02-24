# %%
import sqlite3 as sql
from datetime import datetime
import pandas as pd
import boto3
import boto3.s3
import os
from dotenv import load_dotenv

load_dotenv()

goes_source_bucket = 'noaa-goes18'
nexrad_source_bucket = 'noaa-nexrad-level2'

# %%
session = boto3.Session(
    region_name='us-east-1',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY_SECRET')
)
# %%
s3 = session.resource('s3')
# %%
src_bucket_goes = s3.Bucket(goes_source_bucket)
src_bucket_noaa = s3.Bucket(nexrad_source_bucket)

# %%
def get_all_nexrad_file_name_by_filter_new(year, month, date):
    
    # Log().i(f"User requesting the files for, Station: {station}, Year: {year}, Day: {day}, Hour: {station}")

    # write_nexrad_log(f"User requested the files for, Year: {year}, Month: {month}, Day: {day},  Station: {station}")
    files_available = []
 
    month = '{:02d}'.format(int(month))
    date = '{:02d}'.format(int(date))

    for object_summary in src_bucket_noaa.objects.filter(Prefix=f'{year}/{month}/{date}/'): #/{month}/{day}/{station}
        files_available.append(object_summary.key.split('/')[-1])

    # print("into nexrad filter function")
    # write_nexrad_log(f"File fetched: \n{files_available}")

    return files_available

# %%
def get_all_geos_file_name_by_filter_new(station, year, day, hour):
    # Log().i(f"User requested the files for, Station: {station}, Year: {year}, Day: {day}, Hour: {hour}")
    # write_goes_log(f"User requested the files for, Station: {station}, Year: {year}, Day: {day}, Hour: {hour}")
    files_available=[]
    print('here')

    day = '{:03d}'.format(int(day))
    hour = '{:02d}'.format(int(hour))
    
    for object_summary in src_bucket_goes.objects.filter(Prefix=  f'{station}/{year}/{day}/{hour}/'):
        file_name = object_summary.key.split('/')[-1]
        files_available.append(file_name)
        print(file_name)

    
    # write_goes_log(f"File fetched: \n{files_available}")

    # print("into main get_all_geos_file_name_by_filter")
    # print(files_available)

    return files_available
    

class Metadata:

    def __init__(self):
        self.database_name = 'data/metadata_storage.db'
        self.table_name_goes = 'goes_metadata'
        self.table_name_nexrad = 'nexrad_metadata'

        # creating the database
        self.conn = sql.connect(self.database_name)
        self.cursor = self.conn.cursor()

        # self.create_table_goes()
        # self.create_table_nexrad()

    def truncate_table_data(self):
        str_table_1_drop = "DELETE FROM "+self.table_name_goes
        str_table_2_drop = "DELETE FROM "+self.table_name_nexrad
        self.cursor.execute(str_table_1_drop)
        self.cursor.execute(str_table_2_drop)

    def create_table_goes(self):
        # create sql lite 3 database
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS '''+ self.table_name_goes + ''' (
                station VARCHAR NOT NULL,
                year INTEGER NOT NULL,
                day INTEGER NOT NULL,
                hour INTEGER NOT NULL,
                filename VARCHAR NOT NULL
                ); ''')
        
        print("into create_table_goes")

    def create_table_nexrad(self):
        # create sql lite 3 database
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS '''+ self.table_name_nexrad + ''' (
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                day_of_year INTEGER NOT NULL,
                station_id INTEGER NOT NULL,
                filename VARCHAR NOT NULL
                ); ''')
        
        print("into create_table_nexrad")

    def delete_table_goes(self):
        # delete sql lite 3 database
        self.cursor.execute(''' DROP TABLE IF EXISTS '''+ self.table_name_goes + ''' ; ''')
        
    def delete_table_nexrad(self):
        # delete sql lite 3 database
        self.cursor.execute(''' DROP TABLE IF EXISTS '''+ self.table_name_nexrad + ''' ; ''')

    def insert_data_into_goes(self, station, year, day_of_year, hour, filename):
        insert_str = f'INSERT INTO "{self.table_name_goes}" VALUES("{station}", "{year}", "{day_of_year}", "{hour}", "{filename}");'
        self.cursor.execute(insert_str)


    def insert_data_into_nexrad(self, year, month, date, station_id, filename):
        insert_str1 = f'INSERT INTO "{self.table_name_nexrad}" VALUES("{year}", "{month}", "{date}", "{station_id}", "{filename}");'
        self.cursor.execute(insert_str1)

    def truncate_data_from_nexrad_table(self):
        truncate_str = "DELETE FROM " + self.table_name_nexrad + ";"
        self.cursor.execute(truncate_str)

    def print_and_validate_data_goes(self):
        self.cursor.execute("SELECT * FROM "+ self.table_name_goes)
        rows = self.cursor.fetchall()
        for row in rows:
            # Log().i(row)
            print(row)

    def print_and_validate_data_nexrad(self):
        self.cursor.execute("SELECT * FROM "+ self.table_name_nexrad)
        rows = self.cursor.fetchall()
        for row in rows:
            # Log().i(row)
            print(row)

    def db_conn_close(self):
        self.conn.commit()
        # Log().i('Data entered successfully.')
        self.conn.close()
        if (self.conn):
            self.conn.close()
            # Log().i("The SQLite connection is closed.")

    
    def conn_cursor_function(self):
        return self.conn, self.cursor
    

    def get_goes_table_name(self):
        return self.table_name_goes

    def get_nexrad_table_name(self):
        return self.table_name_nexrad


# %%
metadata_instance = Metadata()



def aws_extract_data_to_sqlite():

    now = datetime.now() 
    day_of_year = '{:03d}'.format(now.timetuple().tm_yday)
    date = '{:02d}'.format(now.timetuple().tm_mday)
    month = '{:02d}'.format(now.timetuple().tm_mon)
    year = '{:04d}'.format(now.timetuple().tm_year)
    hour = '{:02d}'.format(now.timetuple().tm_hour)

    # print('Fetching current date and time ',day, year, hour)

    metadata_instance.truncate_table_data()

    # GOES data 
    station_goes = "ABI-L1b-RadC"

    metadata_instance.create_table_goes()

    # goes_files_available_list = s3_package.get_all_geos_file_name_by_filter_new(station_goes, year, day_of_year, hour)
    print('todays', date, month, year, hour, day_of_year)
    # print('Queried', year, day_of_year, hour)
    goes_files_available_list = get_all_geos_file_name_by_filter_new(station_goes, year, day_of_year, hour)

    try:
        for filename in goes_files_available_list:
            if filename != "" and filename!=None:
                # metadata_instance.insert_data_into_goes(station_goes, year, day_of_year, hour, filename)
                metadata_instance.insert_data_into_goes(station_goes, year, day_of_year,hour, filename)
    except TypeError:
        print("Got NONE TYPE ***GOES*** ")

    # metadata_instance.print_and_validate_data_goes()

    # NEXRAD station
    # metadata_instance.delete_table_nexrad()

    metadata_instance.create_table_nexrad()

    # noaa_filenames_available_list = s3_package_nex.get_all_nexrad_file_name_by_filter(year, month, date)
    noaa_filenames_available_list = get_all_nexrad_file_name_by_filter_new(year, month, date)

    metadata_instance.truncate_data_from_nexrad_table()

    try:
        for filename in noaa_filenames_available_list:
            if filename != "" and filename is not None:
                station_id = str(filename)[0:4]
                # print(station_id, filename)
                # metadata_instance.insert_data_into_nexrad(year, month, date, station_id, filename)
                metadata_instance.insert_data_into_nexrad(year, month, date, station_id, filename)
    except TypeError:
        print("Got NONE TYPE ***NEXRAD*** ")
        

    # metadata_instance.print_and_validate_data_nexrad()


def populate_database():

    conn, cursor = metadata_instance.conn_cursor_function()
    goes_table_name = metadata_instance.get_goes_table_name()
    df1 = pd.read_sql_query("SELECT * FROM "+ goes_table_name, conn )

    nexrad_table_name = metadata_instance.get_nexrad_table_name()
    df2 = pd.read_sql_query("SELECT * FROM "+ nexrad_table_name, conn )

    df1.to_csv('GOES_1.csv',index=False)
    df2.to_csv('NEXRAD_1.csv',index=False)

    metadata_instance.db_conn_close()

# %%
aws_extract_data_to_sqlite()
# %%
