from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands = ['start'], state = '*')
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Введите свое имя")
    await state.set_state("name")


@dp.message_handler(state="name")
async def rename(message: types.Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await message.answer('Введите свой возраст')
    await state.set_state('age')


@dp.message_handler(state='age')
async def age(message: types.Message, state: FSMContext):
    await state.update_data({"age": message.text})
    await message.answer('Добро пожаловать в эхо-бота')
    await state.set_state('message')

@dp.message_handler(state='message')
async def echo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(user_data["name"] + ' ' + user_data["age"] + r' сказал - "' + message.text + r'"')


executor.start_polling(dp, skip_updates=True)


