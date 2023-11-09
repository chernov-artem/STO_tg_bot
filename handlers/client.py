from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardRemove
from keyboards import client_kb
from data_base import sqlite_db
from data_base.sqlite_db import db, sql
from db_functions import *

ID = None

async def commands_start(message : types.Message):
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

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])