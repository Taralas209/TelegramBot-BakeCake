from telegram import ReplyKeyboardMarkup, KeyboardButton
from .static_text import start_button_text, main_menu_button_text, order_buttons
from bake_cake_bot.models import Cake


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
    print('make_main_menu_keyboard')
    buttons = [KeyboardButton(choose) for choose in main_menu_button_text]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_order_menu_keyboard() -> ReplyKeyboardMarkup:
    print('make_order_menu_keyboard')
    buttons = [KeyboardButton(choose) for choose in order_buttons]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_keyboard_for_ready_to_order() -> ReplyKeyboardMarkup:
    print('make_keyboard_for_ready_to_order')
    cakes = Cake.objects.all()
    cake_name = []
    for cake in cakes:
        if cake.ready_to_order:
            cake_name.append(cake.name)

    buttons = [KeyboardButton(choose) for choose in cake_name]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=3),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_shape_keyboard() -> ReplyKeyboardMarkup:
    pass


def make_layer_keyboard() -> ReplyKeyboardMarkup:
    pass


def make_decor_keyboard() -> ReplyKeyboardMarkup:
    pass


def make_berries_keyboard() -> ReplyKeyboardMarkup:
    pass


def make_topping_keyboard() -> ReplyKeyboardMarkup:
    pass