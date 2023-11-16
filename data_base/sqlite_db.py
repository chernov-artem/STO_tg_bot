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
                id INTEGER,
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

async def sql_add_command(ID: int, client_name: str, order_day: str, order_time: str, car:str, telephone: str):
    "функция добавления заказа в базу данных"
    sql.execute(f"UPDATE clients SET client_name = '{client_name}' WHERE id = {ID} ")
    print('вот данные запроса:', ID, client_name, order_day, order_time, car, telephone)
    sql.execute(f"INSERT INTO orders (id, client_name, order_day, order_time, car) VALUES ('{ID}', '{client_name}', '{int(order_day)}', '{order_time}', '{car}')")
    db.commit()
