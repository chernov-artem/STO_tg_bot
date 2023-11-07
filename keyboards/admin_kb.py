# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#
# # Кнопки клавиатуры клиента
# button_work_time = KeyboardButton('/время_работы')
# button_new_order = KeyboardButton('/Записаться_на_ТО')
#
# admin_case_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_work_time).add(button_new_order)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки клавиатуры админа
button_load = KeyboardButton('/Загрузить')
button_detele = KeyboardButton('/Удалить')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_detele)
