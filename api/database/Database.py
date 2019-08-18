import pymysql
import sys

class Database:

    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = "password"
        db = "db"

        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)

        sqls = self.parse_sql('database/sql.sql')

        with self.con.cursor() as cursor:
            for sql in sqls:
                cursor.execute(sql)
                
        
    def parse_sql(self, filename):
        data = open(filename, 'r').readlines()
        stmts = []
        DELIMITER = ';'
        stmt = ''

        for _, line in enumerate(data):
            if not line.strip():
                continue

            if line.startswith('--'):
                continue

            if 'DELIMITER' in line:
                DELIMITER = line.split()[1]
                continue

            if (DELIMITER not in line):
                stmt += line.replace(DELIMITER, ';')
                continue

            if stmt:
                stmt += line
                stmts.append(stmt.strip())
                stmt = ''
            else:
                stmts.append(line.strip())
        return stmts


    def get_users(self):
        sql = "SELECT * FROM user"
        with self.con.cursor() as cursor:
            cursor.execute(sql)
            data = cursor.fetchall()
        return data

    def get_user(self, username, password):
        sql = "SELECT id, username FROM user WHERE username=%s AND password=%s"
        with self.con.cursor() as cursor:
            cursor.execute(sql, (username, password))
            data = cursor.fetchone()
        return data

    def add_user(self, username, password):
        sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
        with self.con.cursor() as cursor:
            cursor.execute(sql, (username, password))
            id = cursor.lastrowid
        self.con.commit()
        return id

    def get_todos(self, user_id):
        sql = "SELECT * FROM todo WHERE user_id=%s"
        with self.con.cursor() as cursor:
            cursor.execute(sql, user_id)
            data = cursor.fetchall()
        return data

    def add_todo(self, title, description, priority, isDone, user_id):
        sql = "INSERT INTO todo (title, description, priority, isDone, user_id) VALUES (%s, %s, %s, %s, %s)"
        isDone = 1 if isDone else 0
        with self.con.cursor() as cursor:
            cursor.execute(sql, (title, description, priority, isDone, user_id))
            id = cursor.lastrowid
        self.con.commit()
        return id


