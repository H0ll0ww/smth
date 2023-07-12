from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, tan
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from sympy import symbols, Eq, solve
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup


b0 = KeyboardButton('Back')
b1 = KeyboardButton(r'/draw_graphic')
b2 = KeyboardButton(r'/clear_board')
b3 = KeyboardButton(r'/set_borders')
b4 = KeyboardButton(r'/get_number_of_crossings')
choose_chat_type_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).insert(b1).insert(b2).add(b3).insert(b4)
back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).insert(b0)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['clear_board'], state='*')
async def clear(message: types.Message):
    plt.clf()
    await message.answer('Доска очищена.', reply_markup=choose_chat_type_keyboard)


@dp.message_handler(commands=['start'], state='*')
async def start_handler(message: types.Message, state: FSMContext):
    await state.update_data(right_border=-10, left_border=10, bottom_border=-10, high_border=10, fst='')
    await message.answer('Добро пожаловать в бота, строящего графики.', reply_markup=choose_chat_type_keyboard)


@dp.message_handler(commands=['draw_graphic'], state='*')
async def get_graph(message: types.Message, state: FSMContext):
    await message.answer('Введите функцию вида y = f(x)', reply_markup=back_keyboard)
    await state.set_state('function')


def create1(s, x):
    return eval(s)


def create(s):
    s = s.replace(' ', '')
    s = s.replace('^', '**')
    s = s[2:]
    n = len(s) - 1
    for i in range(n):
        if s[i].isdigit():
            if s[i+1] == 'x':
                n += 1
                s = s[:i+1] + '*' + s[i+1:]
        elif s[i] == 'x':
            if s[i+1].isdigit():
                n += 1
                s = s[:i+1] + '*' + s[i+1:]
    return s


def my_function(s, x):
    s = s.replace(' ', '')
    s = s.replace('^', '**')
    s = s[2:]
    n = len(s) - 1
    for i in range(n):
        if s[i].isdigit():
            if s[i+1] == 'x':
                n += 1
                s = s[:i+1] + '*' + s[i+1:]
        elif s[i] == 'x':
            if s[i+1].isdigit():
                n += 1
                s = s[:i+1] + '*' + s[i+1:]
    return eval(s)


@dp.message_handler(commands=['get_number_of_crossings'], state='*')
async def get(message: types.Message, state: FSMContext):
    await message.answer('Введите 1-ую функцию вида y = f(x)', reply_markup=back_keyboard)
    await state.set_state('1_function')


@dp.message_handler(state='1_function')
async def get_1(message: types.Message, state: FSMContext):
    if message.text != 'Back':
        await message.answer('Введите 2-ую функцию вида y = f(x)')
        await state.set_state('2_function')
        await state.update_data(fst=message.text)
    else:
        await message.answer('Дейсвие отменено.', reply_markup=choose_chat_type_keyboard)
        await state.set_state('*')


@dp.message_handler(state='2_function')
async def get_2(message: types.Message, state: FSMContext):
    if message.text != 'Back':
        await state.set_state('*')
        data = await state.get_data()
        fst = data['fst']
        await bot.send_message(message.from_id, 'Секунду...')
        scn = create(message.text.lower())
        fst = create(fst.lower())
        x = symbols('x')
        equation = Eq(eval(scn), eval(fst))
        solution = solve(equation, x)
        sorted(solution)
        solutiony = []
        for znach in solution:
            solutiony.append(create1(scn, znach))
        sorted(solutiony)
        x = np.linspace(int(solution[0]) - 5, int(solution[len(solution) - 1]) + 5, 100)
        y = eval(scn)
        plt.plot(x, y)
        y = eval(fst)
        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.ylim(int(solutiony[0]) - 5, int(solutiony[len(solutiony) - 1]) + 5)
        plt.savefig('graph.jpg')
        file = open('graph.jpg', 'rb')
        await bot.send_message(message.from_id, 'Количество пересечений - ' + str(len(solution)))
        await bot.send_message(message.from_id, 'Пересечения при x = ' + str(solution) )
        await message.bot.send_photo(message.from_id, file,
                                     reply_markup=choose_chat_type_keyboard)
        file.close()
    else:
        await message.answer('Введите 1-ую функцию вида y = f(x)')
        await state.set_state('1_function')


@dp.message_handler(commands=['set_borders'], state='*')
async def set_bor(message: types.Message, state: FSMContext):
    await message.answer('Введите правую границу(по x).', reply_markup=back_keyboard)
    await state.set_state('pr_border')


@dp.message_handler(state='pr_border')
async def set_pr(message: types.Message, state: FSMContext):
    if message.text != 'Back':
        await state.set_state('lf_border')
        if message.text.replace(' ', '').replace('-', '').isdigit():
            await bot.send_message(message.from_id, 'Введите левую границу(по x).',)
            await state.update_data(right_border=int(float(message.text.replace(' ', ''))))
    else:
        await message.answer('Действие отменено.')
        await state.set_state('*')


@dp.message_handler(state='lf_border')
async def set_lf(message: types.Message, state: FSMContext):
    if message.text != 'Back':
        await state.set_state('bottom_border')
        if message.text.replace(' ', '').replace('-', '').isdigit():
            await bot.send_message(message.from_id, 'Введите нижнюю границу(по y).',)
            await state.update_data(left_border=int(float(message.text.replace(' ', ''))))
    else:
        await state.set_state('pr_border')
        await message.answer('Введите правую границу(по x).')


@dp.message_handler(state='bottom_border')
async def set_high(message: types.Message, state: FSMContext):
    if message.text != 'Back':
        await state.set_state('high_border')
        if message.text.replace(' ', '').replace('-', '').isdigit():
            await bot.send_message(message.from_id, 'Введите верхнюю границу(по y).',)
            await state.update_data(bottom_border=int(float(message.text.replace(' ', ''))))
    else:
        await state.set_state('lf_border')
        await message.answer('Введите левую границу(по y).')


@dp.message_handler(state='high_border')
async def set_bottom(message: types.Message, state: FSMContext):
    if message.text != 'Back':
        await state.set_state('*')
        if message.text.replace(' ', '').replace('-', '').isdigit():
            await bot.send_message(message.from_id, 'Границы изменены.',
                                   reply_markup=choose_chat_type_keyboard)
            await state.update_data(high_border=int(float(message.text.replace(' ', ''))))
    else:
        await state.set_state('bottom_border')
        await message.answer('Введите нижнюю границу(по y).')


@dp.message_handler(state='function')
async def draw_graph(message: types.Message, state: FSMContext):
    await state.set_state('*')
    if message.text != 'Back':
        await bot.send_message(message.from_id, 'Секунду...')
        data = await state.get_data()
        x = np.linspace(int(data['right_border']), int(data['left_border']),
                        10 * int(data['left_border'] - data['right_border']))
        y = my_function(message.text.lower(), x)
        plt.ylim(int(data['bottom_border']), int(data['high_border']))
        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Graph of ' + message.text)
        plt.grid(True)
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.savefig('graph.jpg')
        file = open('graph.jpg', 'rb')
        await message.bot.send_photo(message.from_id, file,
                                     reply_markup=choose_chat_type_keyboard)
        file.close()
    else:
        await message.answer('Действие отменено.', reply_markup=choose_chat_type_keyboard)


@dp.message_handler(state='*')
async def pst(message: types.Message):
    await message.answer('Если вы хотите воспользоваться ботом, вызовите 1 из предложенных команд.',
                         reply_markup=choose_chat_type_keyboard)


executor.start_polling(dp, skip_updates=True)
