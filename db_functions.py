import sqlite3

db = sqlite3.connect("server.db")
sql = db.cursor()

def create_table_clienst():
    '''Создает таблицу в БД, если она ещё не создана'''
    sql.execute("""CREATE TABLE IF NOT EXISTS clients(
    id INTEGER primary key,
    client_name TEXT)""")
    db.commit()
    print('таблица создана')

def create_table_orders():
    '''Создает таблицу в БД, если она ещё не создана'''
    sql.execute("""CREATE TABLE IF NOT EXISTS orders(
    client_name TEXT,
    order_day TEXT,
    order_time TEXT)""")
    db.commit()
    print('таблица orders создана')

def order_time_chek(day: str, time: str):
    '''Проверяет занятое время. Если врямя занято, возвращает True'''
    sql.execute(f"SELECT client_name FROM orders WHERE order_day = '{day}' AND order_time = '{time}'")
    res = sql.fetchall()
    if res != []:
        return True
    else:
        return False
def sign_up(name):
    """ функция добавления нового клиента"""
    print(type(name), name)
    sql.execute(f"INSERT INTO clients (client_name) VALUES ('{name}')")
    db.commit()
    sql.execute('''SELECT * FROM clients''')
    s = sql.fetchall()
    print(s)

def new_order(name, day, time):
    """ функция записи на прием. Добавляет клиента в базу клиентов, если он записывается в первый раз"""
    sql.execute(f"SELECT * FROM clients WHERE client_name = '{name}'")
    res = sql.fetchall()
    if order_time_chek(day, time):
        print("это время уже занято! выберите другое время")
        return False

    if res != []:
        print(f'Клиента {name} записали {day} дня на {time}')
    else:
        sql.execute(f"INSERT INTO clients (client_name) VALUES ('{name}')")
        print(f"добавили нового клиента {name}. Записали {day} дня на {time}")

    sql.execute(f"INSERT INTO orders (client_name, order_day, order_time) VALUES ('{name}', '{day}', '{time}')")
    db.commit()

def show_client_orders(name: str):
    """ Показывает заказы клиента"""
    sql.execute(f"SELECT * FROM orders WHERE client_name = '{name}'")
    res = sql.fetchall()
    print(res)

def del_client_order(name: str, day :str, time :str):
    sql.execute(f"DELETE FROM orders WHERE client_name = '{name}' AND order_day = '{day}' AND order_time = '{time}'")
    db.commit()
    print(f"Заказ {name} на {day} в {time} удален")

def drop_table():
    ''' Дропает все таблицы и создает их заново'''
    sql.execute('DROP TABLE clients')
    sql.execute('DROP TABLE orders')
    db.commit()
    print('таблица clients и orders дропнуты')
    create_table_clienst()
    create_table_orders()

# sign_up('masha')
# new_order('petia', 5, '12:30')
# new_order('masha', 1, '15:30')
# new_order('vasia', 2, '10:00')
# new_order('petia', 7, '14:00')
# new_order('алколеша', 4, '17:30')
# new_order('алколеша', 4, '17:30')
# new_order('алколеша', 5, '12:35')
# print(order_time_chek(4, '17:30'))
del_client_order('petia', '5', '12:30')
show_client_orders('алколеша')


# drop_table()

