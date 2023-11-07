import sqlite3
from create_bot import bot

db = sqlite3.connect('server.db')
sql = db.cursor()
def sql_start():
    global db, sql

    db = sqlite3.connect('server.db')
    sql = db.cursor()

    if db:
        print("Data base connected OK!")
        '''Создает все таблицы в БД, если оиа ещё не созданы'''
        sql.execute("""CREATE TABLE IF NOT EXISTS clients(
            id INTEGER,
            client_name TEXT,
            cost_sum INTEGER)""")
        sql.execute("""CREATE TABLE IF NOT EXISTS orders(
                client_name TEXT,
                order_day INTEGER,
                order_time TEXT,
                car TEXT,
                cost INTEGER,
                master_name TEXT)""")
        sql.execute("""CREATE TABLE IF NOT EXISTS cars(
            client_name TEXT,
            car_label TEXT,
            car_model TEXT,
            car_year INTEGER NOT NULL,
            car_engine TEXT)""")
        sql.execute("""CREATE TABLE IF NOT EXISTS masters(
            master_name TEXT,
            master_procent INTEGER,
            master_salary INTEGER,
            master_work_days TEXT)""")
        db.commit()
        print('таблицы созданы')



