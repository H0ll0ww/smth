from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup


b1 = KeyboardButton('Да')
b2 = KeyboardButton('Нет')
choose_chat_type_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).insert(b1).insert(b2)
bot = Bot(token = TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
a = []


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message, state: FSMContext):
    global a
    await bot.send_message(message.from_id, 'Добро пожаловать в викторину "Кто ты из Уенсдей"')
    await message.answer('Вопрос 1: Ты носишь только черное?', reply_markup=choose_chat_type_keyboard)
    await state.set_state('answer1')
    a = []


@dp.message_handler(state='answer1')
async def q1(message:types.Message, state:  FSMContext):
    await message.answer('Вопрос 2: Ты моргаешь?', reply_markup=choose_chat_type_keyboard)
    await state.set_state('answer2')
    if message.text == 'Да':
        a.append(1)
    elif message.text == 'Нет':
        a.append(0)


@dp.message_handler(state='answer2')
async def q2(message:types.Message, state:  FSMContext):
    await message.answer('Вопрос 3: Ты знаешь итальянский?', reply_markup=choose_chat_type_keyboard)
    await state.set_state('answer3')
    if message.text == 'Да':
        a.append(1)
    elif message.text == 'Нет':
        a.append(0)


@dp.message_handler(state='answer3')
async def q3(message: types.Message, state: FSMContext):
    await state.set_state('*')
    if message.text == 'Да':
        a.append(1)
    elif message.text == 'Нет':
        a.append(0)
    if a[0] == 0 and a[1] == 0:
        await bot.send_message(message.from_id, 'Ты вещь')
        await message.answer_photo('https://storage.yandexcloud.net/moskvichmag/uploads/2023/01/ruka.jpg')
    elif a[0] == 1 and a[1] == 0 and a[2] == 1:
        await bot.send_message(message.from_id, 'Ты Уэнсдей')
        await message.answer_photo('https://img.championat.com/i/c/c/1670061286629964938.jpg')
    elif a[0] == 1 and a[1] == 0 and a[2] == 0:
        await bot.send_message(message.from_id, 'Ты монстр')
        await message.answer_photo('https://www.soyuz.ru/public/uploads/files/6/7614603/2022112818222855c222bc76.jpg')
    else:
        await bot.send_message(message.from_id, 'Ты просто конченый')
        await message.answer_photo('https://sun9-60.userapi.com/impg/D66bFK4hbReD6aWIXbwz7BRArZ306S1zr8nNcA/KWxqE8QgO_E.jpg?size=604x454&quality=96&sign=adecf7bf094d8717317aed4ef10bb819&c_uniq_tag=7D-aP68J8531sOfRGsNM1Le4Hquj2400npSh5TiQTHQ&type=album')


executor.start_polling(dp, skip_updates=True)