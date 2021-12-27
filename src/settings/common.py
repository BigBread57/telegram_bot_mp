import re

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from src.settings import config, BASE_DIR

storage = MemoryStorage()

bot = Bot(token=config('TOKEN'))
dp = Dispatcher(bot, storage=storage)

DATABASES = {
    'drivername': 'postgresql',
    'database': config('DATABASE'),
    'username': config('USERNAME'),
    'password': config('PASSWORD'),
    'host': config('HOST'),
    'port': config('PORT'),
}

DICT_PM = {}

with open(f'{BASE_DIR}/pm.txt', 'r') as f:
    text = f.read()
text_element = re.findall(r'\w+', text)

key = text_element[::2]
value = text_element[1::2]
for k, v in zip(key, value):
    DICT_PM.update({k: int(v)})
