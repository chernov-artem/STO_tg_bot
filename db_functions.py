import sqlite3

db = sqlite3.connect("server.db")
sql = db.cursor()

def create_table_clients():
    '''Создает таблицу в БД, если она ещё не создана'''
    sql.execute("""CREATE TABLE IF NOT EXISTS clients(
    id INTEGER primary key,
    client_name TEXT,
    cost_sum INTEGER)""")
    db.commit()
    print('таблица создана')

def create_table_orders():
    '''Создает таблицу в БД, если она ещё не создана'''
    sql.execute("""CREATE TABLE IF NOT EXISTS orders(
    client_name TEXT,
    order_day TEXT,
    order_time TEXT,
    car TEXT,
    cost INTEGER)""")
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

def del_client(name: str):
    ''' функция удаления клиента'''
    sql.execute(f"DELETE FROM clients WHERE client_name = '{name}'")
    db.commit()
    sql.execute(f"DELETE FROM orders WHERE client_name = '{name}'")
    db.commit()
    print(f"Клиент {name} удален")

def new_order(name, day, time, car, cost):
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

    sql.execute(f"INSERT INTO orders (client_name, order_day, order_time, car, cost)"
                f" VALUES ('{name}', '{day}', '{time}', '{car}', '{cost}')")
    db.commit()
    refresh(name)

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
    create_table_clients()
    create_table_orders()

def refresh(name: str):
    """ функция обновляет данные в таблицах"""
    sql.execute(f"SELECT cost FROM orders WHERE client_name = '{name}'")
    res = sql.fetchall()
    # считаем сумму за все заказы
    cost_sum = 0
    for i in res:
        cost_sum += i[0]
    print(name, cost_sum)
    sql.execute(f"UPDATE clients SET cost_sum = {cost_sum} WHERE client_name = '{name}'")
    db.commit()


# sign_up('masha')
# new_order('petia', 5, '12:30', 'citro', 11000)
# new_order('masha', 1, '15:30', 'peogeot 207', 7500)
# new_order('vasia', 1, '10:00', 'vaz 2106', 1600)
# new_order('vasia', 2, '11:00', 'vaz 2106', 1200)
# new_order('vasia', 3, '10:30', 'vaz 2106', 3150)
# new_order('vasia', 4, '12:30', 'vaz 2106', 2100)
# new_order('petia', 7, '14:00', 'sub', 14000)
# new_order('алколеша', 4, '17:30', 'volga', 5000)
# new_order('алколеша', 5, '17:30', 'UAZ', 12350)
# new_order('алколеша', 6, '12:35', 'UAZ', 21500)
# print(order_time_chek(4, '17:30'))
# del_client_order('vasia', '2', '11:00')
# show_client_orders('petia')
# del_client('vasia')

# refresh('алколеша')




# drop_table()

# добавить 2 разных мастеров
# добавить парк машин
# добавить возможность добавить/удалить машину клиента
# добавить сумму заказа
# добавить отчисления мастеру за вычетом налогов
# добавить таблицу мастеров