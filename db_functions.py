import sqlite3

db = sqlite3.connect("server.db")
sql = db.cursor()

def create_table():
    '''Создает таблицу в БД, если она ещё не создана'''
    sql.execute("""CREATE TABLE IF NOT EXISTS clients(
    id INTEGER primary key,
    name TEXT)""")
    db.commit()
    print('таблица создана')
def sign_up(name):
    """ функция записи на прием"""
    print(type(name), name)
    sql.execute(f"INSERT INTO clients (name) VALUES ('{name}')")
    db.commit()
    sql.execute('''SELECT * FROM clients''')
    s = sql.fetchall()
    print(s)
    pass

def drop_table():
    sql.execute('DROP TABLE clients')
    db.commit()
    print('таблица clients дропнута')

sign_up('vasia')
# sql.execute("INSERT INTO clients (name) VALUES ('VASIA')")
# db.commit()
# sql.execute("SELECT * FROM clients")
# print(sql.fetchall())
# drop_table()
# create_table()
# sign_up('vasia')
# hui = 'dfwwfr'
# sql.execute("INSERT INTO clients (name) VALUES (?)", (hui))
# db.commit()