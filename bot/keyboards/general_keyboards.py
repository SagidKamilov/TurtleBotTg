from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


'''INLINE-Клавиши'''


def no_registration_keyboard():
    button_cancel = InlineKeyboardButton(text='Я больше не хочу регистрироваться', callback_data='Я больше не хочу регистрироваться')
    keyboard = InlineKeyboardMarkup().add(button_cancel)
    return keyboard


def full_choice_keyboard():
    button_yes = InlineKeyboardButton(text='Да, давай', callback_data='Да, давай')
    button_no = InlineKeyboardButton(text='Нет, не надо', callback_data='Нет, не надо')
    keyboard = InlineKeyboardMarkup().row(button_yes, button_no)
    return keyboard


def short_choice_keyboard_3():
    button_yes = InlineKeyboardButton(text='Да', callback_data='Да3')
    button_no = InlineKeyboardButton(text='Нет', callback_data='Нет3')
    keyboard = InlineKeyboardMarkup().row(button_yes, button_no)
    return keyboard


def short_choice_keyboard_4():
    button_yes = InlineKeyboardButton(text='Да', callback_data='Да4')
    button_no = InlineKeyboardButton(text='Нет', callback_data='Нет4')
    keyboard = InlineKeyboardMarkup().row(button_yes, button_no)
    return keyboard


'''REPLY-Клавиши'''


def full_keyboard(group):
    button1 = KeyboardButton(text=f'Пары {group}')
    button2 = KeyboardButton(text=f'Пары на неделю {group}')
    button3 = KeyboardButton(text='Помощь')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(button1, button2).row(button3)
    return keyboard


def help_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton(text='Помощь'))
