from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardRemove
from keyboards import client_kb
from data_base import sqlite_db
from data_base.sqlite_db import db, sql
from db_functions import *



# from aiogram.dispatcher.filters import Text
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None

class FSMAdmin(StatesGroup):
    """Создаем экземпляры класса машины состояний"""
    client_name = State()
    order_day = State()
    order_time = State()
    car = State()
    telephone = State()
async def commands_start(message : types.Message):
    """стартовая функция
    добавляет ID клиента в базу, если его там ещё нет"""

    ID = message.from_user.id
    try:
        await bot.send_message(message.from_user.id, 'комманд старт клиент: привет!!', reply_markup=client_kb.kb_client)
        await message.delete()
        print('ID пользователя', ID)
        sql.execute(f"SELECT * FROM clients WHERE ID = {ID}")
        if sql.fetchall() == []:
            add_client(ID)
            print('new client!!!')
        # print(sql.fetchall())
    except:
        await message.reply("Общение с ботов в ЛС. Напишите ему @spb9719268STO_bot")

async def work_time(message: types.Message):
    """функция возвращает сообщение с временем работы по кнопке 'цены' """
    ID = message.from_user.id

    await bot.send_message(message.from_user.id, "Время работы с 10:00 до 20:00 ежедневно")

async def costs(message: types.Message):
    """функция возвращает информацию о расценках по кнопке 'цены' """
    ID = message.from_user.id

    await bot.send_message(message.from_user.id, "Нормо-час стоит 1500 рублей\n"
                                                 "малое ТО - 3000 рублей\n"
                                                 "большое ТО 6000 рублей\n"
                                                 "замена насла 1500 рублей\n"
                                                 "и т.д.")

async def make_appointment(message: types.Message):
    """функция добавления заказа, ещё не закончена"""
    ID = message.from_user.id

    await bot.send_message(message.from_user.id, "на прием хотите записаться?")

async def cm_start(message : types.Message, state: FSMContext):
    ID = message.from_user.id
    await FSMAdmin.client_name.set()
    await message.reply("Введите ваше имя:")

async def load_name(message: types.Message, state: FSMContext):
    ID = message.from_user.id
    async with state.proxy() as data:
        data['client_name'] = message.text
    await FSMAdmin.next()
    await  message.reply('Введите день ')

async def load_day(message: types.Message, state: FSMContext):
    ID = message.from_user.id
    async with state.proxy() as data:
        data['order_day'] = message.text
    await FSMAdmin.next()
    await  message.reply('Введите время')

async def load_time(message: types.Message, state: FSMContext):
    ID = message.from_user.id
    async with state.proxy() as data:
        data['order_time'] = message.text
    await FSMAdmin.next()
    await  message.reply('Введите вашу машину')

async def load_car(message: types.Message, state: FSMContext):
    ID = message.from_user.id
    async with state.proxy() as data:
        data['car'] = message.text
    await FSMAdmin.next()
    await  message.reply('Введите ваш телефон')

async def telephone(message: types.Message, state: FSMContext):
    ID = message.from_user.id
    async with state.proxy() as data:
        data['telephone'] = message.text
    await state.finish()
    await sqlite_db.sql_add_command(ID, data['client_name'], data['order_day'], data['order_time'], data['car'], data['telephone'])
    await message.reply(data)
    print(f"ID = {ID}")
    print(f"clien_name = {data['client_name']}")
    print(f"order_day = {data['order_day']}")
    print(f"order_time = {data['order_time']}")
    print(f"car = {data['car']}")
    print(f"telephone = {data['telephone']}")
    for i in data:
        print(data[i])

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(work_time, commands="время_работы")
    dp.register_message_handler(costs, commands="Цены")
    dp.register_message_handler(cm_start, commands=["Записаться_на_ТО"], state=None)
    dp.register_message_handler(load_name, state=FSMAdmin.client_name)
    dp.register_message_handler(load_day, state=FSMAdmin.order_day)
    dp.register_message_handler(load_time, state=FSMAdmin.order_time)
    dp.register_message_handler(load_car, state=FSMAdmin.car)
    dp.register_message_handler(telephone, state=FSMAdmin.telephone)