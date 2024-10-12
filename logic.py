import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database 
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)

        with conn:
            conn.execute('DROP TABLE IF EXISTS project_skills')
            conn.execute('DROP TABLE IF EXISTS projects')
            conn.execute('DROP TABLE IF EXISTS skills')
            conn.execute('DROP TABLE IF EXISTS status')


            conn.commit()   
        print('База данных создана')

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()