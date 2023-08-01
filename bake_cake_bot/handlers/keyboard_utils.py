from telegram import ReplyKeyboardMarkup, KeyboardButton
from .static_text import start_button_text, main_menu_button_text, order_buttons, pay_buttons
from bake_cake_bot.models import Cake, Topping, Shape, Layer, Berries, Decor


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
    shapes = Shape.objects.all()
    shapes_name = []
    for shape in shapes:
        shapes_name.append(shape.name)

    buttons = [KeyboardButton(choose) for choose in shapes_name]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=3),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_layer_keyboard() -> ReplyKeyboardMarkup:
    layers = Layer.objects.all()
    layers_name = []
    for layer in layers:
        layers_name.append(layer.name)

    buttons = [KeyboardButton(choose) for choose in layers_name]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=3),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_decor_keyboard() -> ReplyKeyboardMarkup:
    decors = Decor.objects.all()
    decors_name = []
    for decor in decors:
        decors_name.append(decor.name)
    buttons = [KeyboardButton(choose) for choose in decors_name]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=3),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_berries_keyboard() -> ReplyKeyboardMarkup:
    berries = Berries.objects.all()
    berries_name = []
    for berry in berries:
        berries_name.append(berry.name)
    buttons = [KeyboardButton(choose) for choose in berries_name]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=3),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_topping_keyboard() -> ReplyKeyboardMarkup:
    toppings = Topping.objects.all()
    toppings_name = []
    for topping in toppings:
        toppings_name.append(topping.name)
    buttons = [KeyboardButton(choose) for choose in toppings_name]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=3),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_pay_keyboard() -> ReplyKeyboardMarkup:
    print('make_pay_keyboard')
    buttons = [KeyboardButton(choose) for choose in pay_buttons]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup
