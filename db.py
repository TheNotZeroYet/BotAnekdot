import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        username TEXT,
        joke_ids TEXT,
        password_ids TEXT);
        ''')

        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS jokes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        joke TEXT NOT NULL);
        ''')

        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password TEXT NOT NULL);
        ''')
        self.conn.commit()

    def add_user(self, tg_id, username):
        insert_query = '''
            INSERT INTO users (tg_id, username)
            VALUES (?, ?);
        '''

        user_data = (tg_id, username)
        self.cursor.execute(insert_query, user_data)
        self.conn.commit()

    def add_joke(self, joke):
        insert_query = '''
            INSERT INTO jokes (joke)
            VALUES (?);
        '''

        user_data = (joke)
        self.cursor.execute(insert_query, user_data)
        self.conn.commit()

    def add_password(self, password):
        insert_query = '''
            INSERT INTO passwords (password)
            VALUES (?);
        '''

        user_data = (password)
        self.cursor.execute(insert_query, user_data)
        self.conn.commit()