import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        username TEXT,
        state TEXT,
        joke_ids TEXT,
        password_ids TEXT);
        ''')

        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS jokes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_create_id INTEGER,
        joke TEXT NOT NULL);
        ''')

        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_create_id INTEGER,
        password TEXT NOT NULL);
        ''')
        self.conn.commit()

    def add_user(self, tg_id, username, state):
        insert_query = '''
            INSERT INTO users (tg_id, username, state)
            VALUES (?, ?, ?);
        '''

        user_data = (tg_id, username, state)
        self.cursor.execute(insert_query, user_data)
        self.conn.commit()

    def set_state_user(self, tg_id, state):
        sql = '''UPDATE users SET state = ? WHERE tg_id = ?'''
        self.cursor.execute(sql, (state, tg_id))
        self.conn.commit()

    def get_state_user(self, tg_id):
        sql = f"SELECT state FROM users WHERE tg_id={tg_id}"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result[0]

    def add_joke(self, joke, tg_id):
        insert_query = '''
            INSERT INTO jokes (joke, user_create_id)
            VALUES (?, ?);
        '''

        user_data = (joke, tg_id)
        self.cursor.execute(insert_query, user_data)
        self.conn.commit()

    def add_password(self, password, tg_id):
        insert_query = '''
            INSERT INTO passwords (password, user_create_id)
            VALUES (?, ?);
        '''

        user_data = (password, tg_id)
        self.cursor.execute(insert_query, user_data)
        self.conn.commit()

    def get_last_joke_id(self):
        sql = f"SELECT id FROM jokes"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result[-1][0]

    def get_joke_ids_by_user(self, tg_id):
        sql = f"SELECT joke_ids FROM users WHERE tg_id={tg_id}"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result[0]

    def add_id_joke_to_ids(self, tg_id, joke_id):
        sql = '''UPDATE users SET joke_ids = ? WHERE tg_id = ?'''
        if self.get_joke_ids_by_user(tg_id) is None:
            self.cursor.execute(sql, (f"{joke_id}", tg_id))
        else:
            ids_jokes = self.get_joke_ids_by_user(tg_id)
            self.cursor.execute(sql, (f"{ids_jokes},{joke_id}", tg_id))
        self.conn.commit()