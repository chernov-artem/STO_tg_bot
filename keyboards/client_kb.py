from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки клавиатуры клиента
button_work_time = KeyboardButton('/время_работы')
button_new_order = KeyboardButton('/Записаться_на_ТО')
botton_costs = KeyboardButton('/Цены')
button_start = KeyboardButton('/start')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True).add(button_work_time).add(botton_costs).add(button_new_order).add(button_start)