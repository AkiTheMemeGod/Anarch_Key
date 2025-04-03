import sqlite3 as sq

class Database:
    def __init__(self):
        self.conn = sq.connect('AnarchKey', check_same_thread=False)
        self.cur = self.conn.cursor()

    def user_data(self):
        self.cur.execute("SELECT username,password FROM Account")
        usernames = self.cur.fetchall()
        return dict(usernames)



