from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

"""файл создания бота
т.к. бот тестовый, токен я прописал просто в файле
в рабочих версиях нужно будет сделать чтение токена из файла"""

storage = MemoryStorage()

bot = Bot(token = "6034011497:AAHN0vZgct7hqIFaqK-pp8B4UCybxpD3bzg")
dp = Dispatcher(bot, storage=storage)