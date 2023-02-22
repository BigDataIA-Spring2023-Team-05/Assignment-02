# %%
import sqlite3 as sql
import os
from utils.logger import Log as log
from pathlib import Path

# %%
class User:

    def __init__(self) -> None:
        self.database_name = 'assignment_2.db'
        self.ddl_file = 'ddl.sql'
        self.table_name = 'users'

        self.database_file_path = os.path.join(os.path.dirname(__file__), self.database_name)
        self.ddl_file_path = os.path.join(os.path.dirname(__file__), self.ddl_file)
        
        self.is_database_initilization()

    
    def create_database(self):
        with open(self.ddl_file_path, 'r') as sql_file:
            sql_script = sql_file.read()
        
        db = sql.connect(self.database_file_path, check_same_thread=False)
        cursor = db.cursor()
        cursor.executescript(sql_script)
        db.commit()
        db.close()
        log().i('Database initialized succesfully!')

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


    def is_database_initilization(self):
        if not Path(self.database_file_path).is_file():
            log().i('Database file not found, initilizing...')
            self.create_database()
        else:
            log().i('Database file already exist')

    
    def insert_new_user(self, username: str, passphrase: str) -> bool:
        try:
            self.db_open_connection()
            insert_str = f'INSERT INTO users (username, passphrase) VALUES ("{username}", "{passphrase}");'
            self.cursor.execute(insert_str)
            return True
        except sql.IntegrityError as er:
            log().i(f'SQLite error for {username}: %s' % (' '.join(er.args)))
            return False
        finally:
            self.db_close_connection()

    def find_username(self, username: str):
        try:
            self.db_open_connection()
            query = f'SELECT * FROM users WHERE username="{username}";'
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if(len(result) == 0):
                return None
            
            return {'id': result[0][0], 'username': result[0][1], 'password': result[0][2]}
        
        except sql.Error as er:
            log().i('SQLite error: %s' % (' '.join(er.args)))
            log().i('SQLite traceback: ')


# %%
if __name__ == "__main__":
    user = User()
    # log().i(str(user.insert_new_user('admin2', 'admin2')))
    print(user.find_username('admin'))
    print(user.find_username('admin3'))


