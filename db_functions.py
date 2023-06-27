import sqlite3
from random import choice

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

    if not chek_car(name, car_label, car_model, car_year, car_engine):
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
    if chek_car(name, car_label, car_model, car_year, car_engine):
        sql.execute(f"DELETE FROM cars WHERE client_name = '{name}'"
                f" AND car_label = '{car_label}' AND car_model = '{car_model}'"
                f"AND car_year = '{car_year}' AND car_engine = '{car_engine}'")
        db.commit()
        print("Машина удалена")
    else:
        print("Такой машины нет в гараже")
def chek_car(name: str, car_label: str, car_model: str, car_year: int, car_engine: str) -> bool:
    """ функция проверяет наличие машины в гараже"""
    sql.execute(f"SELECT * FROM cars WHERE client_name = '{name}'"
                f" AND car_label = '{car_label}' AND car_model = '{car_model}'"
                f"AND car_year = '{car_year}' AND car_engine = '{car_engine}'")
    res = sql.fetchall()
    if res == []:
        return False
    else:
        return True

def add_master(master_name: str, master_procent: int, master_salary: int, master_work_days: str):
    """ Добавляет нового мастера в базу данных (если такого ещё нет)"""
    if not master_chek(master_name, master_procent, master_salary, master_work_days):
        sql.execute(
            f"""INSERT INTO masters (master_name, master_procent, master_salary, master_work_days)
            VALUES ('{master_name}', {master_procent}, {master_salary}, '{master_work_days}')""")
        db.commit()
        print(f"Добавили мастера {master_name} в базу")
    else:
        print(f"Мастер {master_name} уже зерегистрирован в базе")
def del_master(master_name: str, master_procent: int, master_salary: int, master_work_days: str):
    if master_chek(master_name, master_procent, master_salary, master_work_days):
        sql.execute(f"""DELETE FROM masters WHERE master_name = '{master_name}'""")
        db.commit()
        print(f"Мастер {master_name} удален из базы")
    else:
        print(f"Мастера {master_name} нет в базе данных")
def master_chek(master_name: str, master_procent: int, master_salary: int, master_work_days: str) -> bool:
    """ проверяет наличия мастера в базе"""
    sql.execute(f"SELECT * FROM masters WHERE master_name = '{master_name}'")
    res = sql.fetchall()

    if not res == []:
        return True
    else:
        return False

def busy_master(master_name: str, day: int) -> bool:
    """возвращает True если мастер сегодня работает"""
    sql.execute(f"SELECT master_name, master_work_days FROM masters WHERE master_name = '{master_name}'")
    res = sql.fetchall()
    work_days_temp = res[0][1][1:-1]
    work_days = work_days_temp.replace(' ', '')
    x = work_days.split(',')
    work_days_int = []
    for i in x:
        work_days_int.append(int(i))
    if day in work_days_int:
        return True
    else:
        return False

def master_free(day: int) -> list:
    """ возвращает список работающих в данный день мастеров"""
    sql.execute("SELECT master_name FROM masters")
    res = sql.fetchall()
    master_list = []
    for i in res:
        if busy_master(i[0],day):
            master_list.append(i[0])
    return master_list

def random_master(day: int, time: str) -> str|bool:
    """ выбирает из работающих сегодня мастеров рандомного мастера и даёт ему заказ"""
    master_free_list = master_free(int(day))
    print('master_free_list = ', master_free_list)
    sql.execute(f"SELECT master_name FROM orders WHERE order_day = {day} AND order_time = '{time}'")
    busy_masters_tmp = sql.fetchall()
    print('busy_masters_tmp = ', busy_masters_tmp, 'day ', day, 'time ', time)
    # преобразуем элементы списка из кортежей в строки
    busy_masters = []
    for i in busy_masters_tmp:
        busy_masters.append(i[0])
    print('бизи мастерс = ', busy_masters)

    # вычитаем списки
    res = [i for i in master_free_list if i not in busy_masters]
    print('free_masters_list', res)

    if res == []:
        return False
    else:
        return choice(res)




def add_car_name_to_order(name: str, car: int):
    """функция проверяет наличие машины в таблице cars
    возвращает информацию о машине выбранного номера машины
    т.е. если car = 1 возврощает машину1 и т.д.
    если машин нет, возвращет unknow """
    sql.execute(f"SELECT * FROM cars WHERE client_name = '{name}'")
    res = sql.fetchall()

    if car in range(len(res)):
        if res[car][1] == 'none':
            return "?"
        else:
            return res[car][1] + " " + res[car][2] + " " + str(res[car][3]) + " " + res[car][4]
    else:
        return False

def new_order(name, day, time, car, cost):
    """ функция записи на прием. Добавляет клиента в базу клиентов, если он записывается в первый раз
    для добавления заказа нужно выбрать машину из своего гаража. Если машины ещё нет, нужно добавить свою машину в гараж"""

    # получаем рандомного свободного мастера
    master = random_master(day, time)
    if master:
        pass
    else:
        print("На это время нет свободных мастеров")
        return False
    # проверяем наличие клиента в базе, если его нет - добавляем
    sql.execute(f"SELECT * FROM clients WHERE client_name = '{name}'")
    res = sql.fetchall()

    if res != []:
        print(f'Клиента {name} записали {day} дня на {time} Мастер {master}')
    else:
        add_client(name)
        print(f"добавили нового клиента {name}. Записали {day} дня на {time} Мастер {master}")

    sql.execute(f"INSERT INTO orders (client_name, order_day, order_time, car, cost, master_name)"
                f" VALUES ('{name}', '{day}', '{time}', '{car}', '{cost}', '{master}')")
    db.commit()
    refresh(name, master)

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
    sql.execute('DROP TABLE masters')
    db.commit()
    print('таблица clients, orders, car и masters дропнуты')
    create_tables()

def refresh(name: str, master: str):
    """ функция обновляет данные в таблицах"""
    sql.execute(f"SELECT cost FROM orders WHERE client_name = '{name}'")
    res = sql.fetchall()
    # считаем сумму за все заказы
    cost_sum = 0
    for i in res:
        cost_sum += i[0]
    print(name, cost_sum)
    sql.execute(f"UPDATE clients SET cost_sum = {cost_sum} WHERE client_name = '{name}'")
    # считаем отчисления мастеру
    sql.execute(f"SELECT cost FROM orders WHERE master_name = '{master}'")
    res_master = sql.fetchall()
    master_salary_tmp = 0
    for i in res_master:
        master_salary_tmp += i[0]
    sql.execute(f"SELECT master_procent FROM masters WHERE master_name = '{master}'")
    master_procent = sql.fetchall()[0][0]
    print('master_procent ', master_procent)
    master_salary = (master_salary_tmp * int(master_procent) / 100) * 0.87
    sql.execute(f"UPDATE masters SET master_salary = {int(master_salary)} WHERE master_name = '{master}'")
    db.commit()

# add_client('masha')
# add_car('masha', 'peugeot', '207', 2010, '1,6')
# add_car('masha', 'sitroen', 'c1', 2013, '1,4')
# new_order('petia', 5, '12:30', 'citro', 11000)
# new_order('masha', 5, '14:30', 'peugeot 207', 7500)
# new_order('vasia', 1, '10:00', 'vaz 2106', 1600)
# add_master('Масик', 35, 0, '[1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22, 25, 26, 29, 30]')
# add_master('Вова', 40, 0, '[1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22, 25, 26, 29, 30]')
# add_master('ALKOлеша', 40, 0, '[3, 4, 7, 8, 11, 12, 15, 16, 19, 20, 23, 24, 27, 28, 31]')
# add_master('Саня', 45, 0, '[3, 4, 7, 8, 11, 12, 15, 16, 19, 20, 23, 24, 27, 28, 31]')





# new_order('vasia', 2, '11:00', 'vaz 2106', 1200)
# new_order('vasia', 3, '10:30', 'vaz 2106', 3150)
new_order('vasia', 6, '12:30', 'vaz 2106', 2100)
# new_order('petia', 7, '14:00', 'sub', 14000)
# print(chek_car('masha', ''))

# print(master_free(3))
# print(master_free(2))
# print(busy_master('Масик', 9))
# print(busy_master('Вова', 9))
# print(busy_master('ALKOлеша', 9))
# print(busy_master('Саня', 9))

# random_master(5, '15:30')
# print(random_master(1, '15:30'))

# print(order_time_chek(4, '17:30'))
# del_client_order('vasia', '2', '11:00')
# show_client_orders('petia')
# del_client('vasia')

# print(master_chek('масик', 35, 0, '[1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22, 25, 26, 29, 30]'))
# master_chek('масик', 35, 0, '[3, 4, 7, 8, 11, 12, 15, 16, 19, 20, 23, 24, 27, 28, 31]')

# refresh('алколеша')
# create_tables()
# drop_table()

# добавить 2 разных мастеров


# добавить сумму заказа
# добавить отчисления мастеру за вычетом налогов
# добавить возможность редактирования в таблице cars
# добавить возможность редактирования в таблице clients
# добавить возможность редактирования в таблице masters
# добавить возможность редактирования в таблице orders
