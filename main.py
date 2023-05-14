""" Телеграм бот для записи на автосервис"""

import requests
from datetime import datetime
import telebot
import sqlite3
from aiogram import bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


token = "6034011497:AAHN0vZgct7hqIFaqK-pp8B4UCybxpD3bzg"
db = sqlite3.connect("server.db")
sql = db.cursor()

def create_table():
    sql.execute("""CREATE TABLE IF NOT EXISTS clients(
    name TEXT,
    day TEXT,
    time TEXT)""")
    db.commit()
    print('таблица создана')


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Hello!")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text == "l":
            bot.send_message(message.chat.id, "test ok")
        elif message.text == "1":
            bot.send_message(message.chat.id, "Введите день:")
            if message.text == "1":
                bot.send_message(message.chat.id, 'выбран день 1')
            else:
                bot.send_message(message.chat.id, 'день не выбран')

        else:
            bot.send_message(
                message.chat.id,
                "chek the command"
            )
            bot.send_message(message.chat.id, "Введите команду")


    bot.polling()

if __name__ == '__main__':
    # get_date()
    create_table()
    telegram_bot(token)

