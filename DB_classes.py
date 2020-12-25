import sqlite3
import datetime

def get_table_form(params):
    text = "("
    for item in params:
        text += item + ","
    text = text[:-1] + ")"
    return text

def get_insert_format(table, params, table_params):
    req = "INSERT INTO {} {} VALUES (".format(table, get_table_form(table_params))
    for item in params:
        req += '"{}",'.format(item)
    req = req[:-1] + ");"
    return req

class DataBase:
    """Создавать и использовать только в одной функции. Нельзя делать свойством другого класса."""
    def __init__(self):
        self.conn = sqlite3.connect("work.db")
        self.cursor = self.conn.cursor()
        self.create_all_tables()

    def create_all_tables(self):
        """Создает все необходимые таблицы"""
        # Сотрудник
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS workers
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        is_confidential INT,
        contacts TEXT,
        education TEXT,
        post_id INTEGER,
        workplace_id INTEGER
        );""")
        # Место работы
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS workplace
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        monitor INTEGER,
        level INTEGER,
        address TEXT
        );""")
        # Должность
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS post
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        salary REAL,
        vacancy_rate INT
        );""")

    def execute_and_commit(self, request):
        self.cursor.execute(request)
        self.conn.commit()

    def add_item(self, table, params, table_params):
        """Добавляет в нужную таблицу какие-либо данные ( params )"""
        request_insert = get_insert_format(table, params, table_params)
        self.execute_and_commit(request_insert)

    def select_item(self, table, id = None):
        request = "SELECT * FROM {}".format(table)
        if id is not None:
            request += " WHERE id == {};".format(id)
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def delete_item(self, table, id):
        request = "DELETE FROM {} WHERE id == {}".format(table, id)
        self.execute_and_commit(request)

    def get_id(self, table):
        request = "SELECT * FROM {}".format(table)
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        arr = []
        for item in result:
            arr.append(item[0])
        return arr
