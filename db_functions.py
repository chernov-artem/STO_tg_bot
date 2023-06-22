import sqlite3

db = sqlite3.connect("server.db")
sql = db.cursor()

def create_tables():
    '''Создает все таблицы в БД, если оиа ещё не созданы'''
    sql.execute("""CREATE TABLE IF NOT EXISTS clients(
    id INTEGER primary key,
    client_name TEXT,
    cost_sum INTEGER)""")
    sql.execute("""CREATE TABLE IF NOT EXISTS orders(
        client_name TEXT,
        order_day TEXT,
        order_time TEXT,
        car TEXT,
        cost INTEGER)""")
    sql.execute("""CREATE TABLE IF NOT EXISTS cars(
    client_name TEXT,
    car_label TEXT,
    car_model TEXT,
    car_year INTEGER NOT NULL,
    car_engine TEXT)""")
    db.commit()
    print('таблицы созданы')


def order_time_chek(day: str, time: str):
    '''Проверяет занятое время. Если врямя занято, возвращает True'''
    sql.execute(f"SELECT client_name FROM orders WHERE order_day = '{day}' AND order_time = '{time}'")
    res = sql.fetchall()
    if res != []:
        return True
    else:
        return False
def add_client(name):
    """ функция добавления нового клиента
    нельзя добавить клиента, если имя уже занято"""

    if not chek_client(name):
        sql.execute(f"INSERT INTO clients (client_name) VALUES ('{name}')")
        sql.execute(
            f"""INSERT INTO cars (client_name, car_label, car_model, car_year, car_engine)
                 VALUES ('{name}', 'none', 'none', 1900, 'none')""")
        db.commit()
    else:
        print('Такой клиент уже зарегистрирован')
    sql.execute('''SELECT * FROM clients''')
    s = sql.fetchall()
    print(s)

def del_client(name: str):
    ''' функция удаления клиента'''

    if chek_client(name):
        sql.execute(f"DELETE FROM clients WHERE client_name = '{name}'")
        sql.execute(f"DELETE FROM orders WHERE client_name = '{name}'")
        sql.execute(f"DELETE FROM cars WHERE client_name = '{name}'")
        db.commit()
        print(f"Клиент {name} удален")
    else:
        print(f"Клиент {name} не зарегистрирован в базе")


def chek_client(name: str) -> bool:
    sql.execute(f"SELECT * FROM clients WHERE client_name = '{name}'")
    res = sql.fetchall()
    if res == []:
        return False
    else:
        return True

def add_car(name: str, car_label: str, car_model: str, car_year: int, car_engine: str):
    """ функция добавляет машину, если её ещё нет в гараже"""

    if not chek_car0(name, car_label, car_model, car_year, car_engine):
        sql.execute(
            f"""INSERT INTO cars (client_name, car_label, car_model, car_year, car_engine) VALUES ('{name}', '{car_label}', '{car_model}', {car_year}, '{car_engine}')""")
        db.commit()
        print(
            f"Для клиента {name} добавлен автомобиль {car_label} {car_model} {car_year} года c двигателем {car_engine} ")
    else:
        print("этот автомобиль уже зарегистрирован в гараже")
        print(f"А если у клиента несколько одинаковых машин, назовите их {car_label}1, {car_label}2 и т.д.")

def del_car(name: str, car_label: str, car_model: str, car_year: int, car_engine: str):
    """ функция удаляет машину, если она уже есть в гараже"""
    if chek_car0(name, car_label, car_model, car_year, car_engine):
        sql.execute(f"DELETE FROM cars WHERE client_name = '{name}'"
                f" AND car_label = '{car_label}' AND car_model = '{car_model}'"
                f"AND car_year = '{car_year}' AND car_engine = '{car_engine}'")
        db.commit()
        print("Машина удалена")
    else:
        print("Такой машины нет в гараже")


def chek_car0(name: str, car_label: str, car_model: str, car_year: int, car_engine: str) -> bool:
    """ функция проверяет наличи машины в гараже"""
    sql.execute(f"SELECT * FROM cars WHERE client_name = '{name}'"
                f" AND car_label = '{car_label}' AND car_model = '{car_model}'"
                f"AND car_year = '{car_year}' AND car_engine = '{car_engine}'")
    res = sql.fetchall()
    if res == []:
        return False
    else:
        return True
def chek_car(name: str, car: int):
    """функция проверяет наличие машины в таблице cars
    возвращает информацию о машине выбранного номера машины
    т.е. если car = 1 возврощает машину1 и т.д.
    если машин нет, возвращет unknow """
    sql.execute(f"SELECT * FROM cars WHERE client_name = '{name}'")
    res = sql.fetchall()
    print('res = ', res)
    print(res[0], type(res[0]))

    if car in range(20) and res == []:
        return "unknow"
    elif car in range(20):
        return res[car][1] + " " + res[car][2] + " " + str(res[car][3]) + " " + res[car][4]
    else:
        return False

def new_order(name, day, time, car, cost):
    """ функция записи на прием. Добавляет клиента в базу клиентов, если он записывается в первый раз
    для добавления заказа нужно выбрать машину из своего гаража. Если машины ещё нет, нужно добавить свою машину в гараж"""
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
    sql.execute('DROP TABLE cars')
    db.commit()
    print('таблица clients, orders и car дропнуты')
    create_tables()

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

# add_client('masha')
# add_car('masha', 'peugeot1', '207', 2010, '1,6')
# print(chek_car0('masha', 'peugeot2', '207', 2010, '1,6'))
# del_car('masha', 'peugeot1', '207', 2010, '1,6')
# add_car('masha', 'sitroen', 'c1', 2013, '1,4')
# new_order('petia', 5, '12:30', 'citro', 11000)
# new_order('masha', 1, '15:30', 'peugeot 207', 7500)
# new_order('vasia', 1, '10:00', 'vaz 2106', 1600)
# new_order('vasia', 2, '11:00', 'vaz 2106', 1200)
# new_order('vasia', 3, '10:30', 'vaz 2106', 3150)
# new_order('vasia', 4, '12:30', 'vaz 2106', 2100)
# new_order('petia', 7, '14:00', 'sub', 14000)
# new_order('алколеша', 4, '17:30', 'volga', 5000)
# new_order('алколеша', 5, '17:30', 'UAZ', 12350)
# new_order('алколеша', 6, '12:35', 'UAZ', 21500)
# print(chek_car('masha', ''))

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