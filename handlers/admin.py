from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardRemove
from keyboards import admin_kb
from data_base import sqlite_db


# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram import types, Dispatcher
# from create_bot import dp, bot
# from aiogram.dispatcher.filters import Text
# from data_base import sqlite_db
# from keyboards import admin_kb



ID = None

# Получаем права админа
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'привет админ', reply_markup=admin_kb.button_case_admin)
async def commands_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'комманд старт админ: привет!', reply_markup=admin_kb.button_case_admin)
        await message.delete()
    except:
        await message.reply("Общение с ботом в ЛС. Напишите ему @spb9719268STO_bot")

def register_handlers_admin(dp : Dispatcher):

    dp.register_message_handler(commands_start, commands=['start', 'help1'])
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)