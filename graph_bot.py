from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
import matplotlib.pyplot as plt
import numpy as np
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from sympy import symbols, Eq, solve


a = 10
fst = ''
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['clear_board'], state='*')
async def clear(message: types.Message, state: FSMContext):
    plt.clf()
    await message.answer('Доска очищена.')


@dp.message_handler(commands=['start'], state='*')
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer('Добро пожаловать в бота, строящего графики.')


@dp.message_handler(commands=['draw_graphic'], state='*')
async def get_graph(message: types.Message,state: FSMContext):
    await message.answer('Введите функцию вида y = f(x)')
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
    await message.answer('Введите 1-ую функцию вида y = f(x)')
    await state.set_state('1_function')


@dp.message_handler(state='1_function')
async def get_1(message: types.Message, state: FSMContext):
    global fst
    await message.answer('Введите 2-ую функцию вида y = f(x)')
    await state.set_state('2_function')
    fst = message.text


@dp.message_handler(state='2_function')
async def get_2(message: types.Message, state: FSMContext):
    await state.set_state('*')
    global fst
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
    plt.xlabel = 'x'
    plt.ylabel = 'y'
    plt.grid = True
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.ylim(int(solutiony[0]) - 5, int(solutiony[len(solutiony) - 1]) + 5)
    plt.savefig('graph.jpg')
    file = open('graph.jpg', 'rb')
    await bot.send_message(message.from_id, 'Количество пересечений - ' + str(len(solution)))
    await bot.send_message(message.from_id, 'Пересечения при x = ' + str(solution) )
    await message.bot.send_photo(message.from_id, file)
    file.close()


@dp.message_handler(commands=['set_borders'], state='*')
async def set(message: types.Message, state: FSMContext):
    await message.answer('Введите 1 целое число.')
    await state.set_state('border')


@dp.message_handler(state='border')
async def set_bor(message: types.Message, state: FSMContext):
    global a
    await state.set_state('*')
    if message.text.replace(' ', '').isdigit():
        await bot.send_message(message.from_id, 'Границы доски изменены.')
        a = int(message.text.replace(' ', ''))


@dp.message_handler(state='function')
async def draw_graph(message: types.Message, state: FSMContext):
    await state.set_state('*')
    await bot.send_message(message.from_id, 'Секунду...')
    global a
    x = np.linspace(-a, a, 10 * a)
    y = my_function(message.text.lower(), x)
    plt.ylim(-a, a)
    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Graph of ' + message.text)
    plt.grid(True)
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.savefig('graph.jpg')
    file = open('graph.jpg', 'rb')
    await message.bot.send_photo(message.from_id, file)
    file.close()


executor.start_polling(dp, skip_updates=True)
