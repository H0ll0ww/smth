import asyncio
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
import requests
import random


mass = []
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)
fndprs = []
dictionary = {}


@dp.message_handler(commands = ['start'])
async def start_handler(message: types.Message):
    await message.answer("Вы вступили в анонимный груповой чат")
    if message.from_id not in mass:
        mass.append(message.from_id)
        dictionary[str(message.from_id)] = -1


@dp.message_handler(commands = ['find_person'])
async def find_person(message: types.Message):
    if len(fndprs) == 0:
        fndprs.append(message.from_id)
    else:
        id = fndprs.pop(random.randint(0, len(fndprs) - 1))
        dictionary[str(id)] = message.from_id
        dictionary[str(message.from_id)] = id
        await bot.send_message(id, 'Чат 1 на 1 начался')
        await bot.send_message(message.from_id, 'Чат 1 на 1 начался')


@dp.message_handler(commands = ['get_random_cat'])
async def get_cat(message: types.Message):
    response = requests.get('https://api.thecatapi.com/v1/images/search').json()
    url = response[0]['url']
    await message.answer_photo(url)


@dp.message_handler(commands=['close_chat'])
async def close_chat(message: types.Message):
    id = dictionary[str(message.from_id)]
    await bot.send_message(id, 'Один из участников завершил чат')
    await bot.send_message(message.from_id, 'Один из участников завершил чат')
    dictionary[str(message.from_id)] = -1
    dictionary[str(id)] = -1


@dp.message_handler()
async def send_messages(message: types.Message):
    mess = []
    if dictionary[str(message.from_id)] != -1:
        await bot.send_message(dictionary[str(message.from_id)], message.text)
    else:
        for i in range(len(mass)):
            if mass[i] != message.from_id:
                if dictionary[str(mass[i])] == -1:
                    mess.append(bot.send_message(mass[i], message.text))
        await asyncio.gather(*mess)


executor.start_polling(dp, skip_updates = True)