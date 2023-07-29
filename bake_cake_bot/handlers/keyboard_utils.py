from telegram import ReplyKeyboardMarkup, KeyboardButton
from .static_text import start_button_text, main_menu_button_text


def build_menu(buttons, n_cols):
    return [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]


def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    print('make_keyboard_for_start_command')
    buttons = [KeyboardButton(button) for button in start_button_text]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=1),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_main_menu_keyboard() -> ReplyKeyboardMarkup:
    print('make_customer_keyboard')
    buttons = [KeyboardButton(choose) for choose in main_menu_button_text]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


