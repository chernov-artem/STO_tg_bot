from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardRemove
from keyboards import admin_kb
from data_base import sqlite_db

"""обработка команд для админа"""

ID = None

# Получаем права админа
async def make_changes_command(message: types.Message):
    """функция обработки кнопки 'модератор' """
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'привет админ', reply_markup=admin_kb.button_case_admin)
async def commands_start(message : types.Message):
    """стартовая функция"""
    try:
        await bot.send_message(message.from_user.id, 'комманд старт админ: привет!', reply_markup=admin_kb.button_case_admin)
        await message.delete()
    except:
        await message.reply("Общение с ботом в ЛС. Напишите ему @spb9719268STO_bot")

def register_handlers_admin(dp : Dispatcher):

    dp.register_message_handler(commands_start, commands=['start', 'help1'])
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)