from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


b0 = KeyboardButton('Back')
b1 = KeyboardButton(r'/draw_graphic')
b2 = KeyboardButton(r'/clear_board')
b3 = KeyboardButton(r'/set_borders')
b4 = KeyboardButton(r'/get_number_of_crossings')
b5 = KeyboardButton(r'/derivative')
choose_chat_type_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).insert(b1).insert(b2).add(b3).insert(b4).add(b5)
back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).insert(b0)