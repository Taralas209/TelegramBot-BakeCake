from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from . import static_text
from bake_cake_bot.models import Users, Cake, Shape, Layer, Topping, Decor, Berries
from .keyboard_utils import make_keyboard_for_start_command, make_main_menu_keyboard, make_order_menu_keyboard, \
    make_keyboard_for_ready_to_order, make_decor_keyboard, make_shape_keyboard, make_berries_keyboard, \
    make_topping_keyboard, make_layer_keyboard


AUTH, CREATE_USER, USER_PHONE, MAIN_MENU, ORDER, ORDER_CAKE, LAYER, DECOR, TOPPING, BERRIES, CALCULATE = range(11)


def command_start(update: Update, context):
    print('command_start')
    if update.message:
        user_info = update.message.from_user.to_dict()
    else:
        user_info = {'id': context.user_data['user_id'], 'username': context.user_data['username'],
                     'first_name': context.user_data['first_name']}

    user, created = Users.objects.get_or_create(telegram_id=user_info['id'])

    if created:
        text = static_text.start_created.format(first_name=user_info['first_name'])
    else:
        text = static_text.start_not_created.format(first_name=user_info['first_name'])

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=make_keyboard_for_start_command(),
    )
    return AUTH


def get_auth_info(update: Update, _: CallbackContext):
    auth = update.message.text
    if auth == static_text.start_button_text[0]:
        print('Auth pressed')
        user_info = update.message.from_user.to_dict()
        user = Users.objects.get(telegram_id=user_info['id'])
        if not user.phone:
            print('registration_request')
            update.message.reply_text(static_text.need_auth)
            with open('./static/agreement.txt', 'r') as agreement:
                update.message.reply_document(document=agreement)
            update.message.reply_text(text=static_text.name)
            return CREATE_USER
        else:
            update.message.reply_text(text=static_text.choose_option, reply_markup=make_main_menu_keyboard())
            return MAIN_MENU


def create_user(update: Update, user_description):
    print('create_user, get name')
    user_description.bot_data['name'] = update.message.text
    update.message.reply_text(text=static_text.phone)
    return USER_PHONE


def get_user_phone(update: Update, user_description):
    print('create_user, get phone')
    user_info = update.message.from_user.to_dict()
    user = Users.objects.get(telegram_id=user_info['id'])
    user.phone = update.message.text
    if user.phone.is_valid():
        user.name = user_description.bot_data['name']
        user.save()
        update.message.reply_text(text=static_text.user_saved)
        update.message.reply_text(text=static_text.choose_option, reply_markup=make_main_menu_keyboard())
        return MAIN_MENU
    else:
        update.message.reply_text(static_text.correct_phone)
        return USER_PHONE


def get_main_menu(update: Update, _):
    print('get_customer_menu')
    customer_choise = update.message.text
    if customer_choise == static_text.main_menu_button_text[0]:
        print('get_order')
        update.message.reply_text(text=static_text.ready_to_order)
        cakes = Cake.objects.all()
        for cake in cakes:
            if cake.ready_to_order:
                ready_to_order_cake = (
                    f'{cake.name}\n'
                    f'------------\n'
                    f'Количество слоев - {cake.layer}\n'
                    f'Форма - {cake.shape}\n'
                    f'Топпинг - {cake.topping}\n'
                    f'Ягоды - {cake.berries}\n'
                    f'Декор - {cake.decor}\n'
                    f'Текст на торте - {cake.text}\n'
                    f'------------\n'
                    f'Цена - {cake.price}ру.'
                )
                update.message.reply_text(text=ready_to_order_cake, reply_markup=make_order_menu_keyboard())
        return ORDER
    elif customer_choise == static_text.main_menu_button_text[1]:
        update.message.reply_text(text='ТУТ БУДЕТ МЕНЮ ПРОВЕРИТЬ ЗАКАЗ')
        return MAIN_MENU
    elif customer_choise == static_text.main_menu_button_text[2]:
        update.message.reply_text(text='ТУТ БУДЕТ МЕНЮ ИСТОРИЯ ЗАКАЗОВ')
        return MAIN_MENU
    elif customer_choise == static_text.main_menu_button_text[3]:
        update.message.reply_text(text=static_text.contacts)
        update.message.reply_text(text=static_text.something_else, reply_markup=make_main_menu_keyboard())
        return MAIN_MENU
    else:
        update.message.reply_text(text=static_text.not_text_enter, reply_markup=make_main_menu_keyboard())
        return MAIN_MENU # Вернет меню на случай ручного ввода


def get_order(update: Update, cake_description):
    customer_choise = update.message.text
    if customer_choise == static_text.order_buttons[0]:
        update.message.reply_text(text=static_text.ready_order, reply_markup=make_keyboard_for_ready_to_order())
        update.message.reply_text(text=static_text.ordering)
        update.message.reply_text(text=static_text.address)
        return ORDER_CAKE
    elif customer_choise == static_text.order_buttons[1]:
        update.message.reply_text(text=static_text.individual_order)
        update.message.reply_text(text=static_text.select_shape, reply_markup=make_shape_keyboard())
        return LAYER
    else:
        return MAIN_MENU # Вернет меню на случай ручного ввода


def get_layer(update: Update, cake_description):
    cake_description.bot_data['shape'] = update.message.text
    update.message.reply_text(text=static_text.select_layers, reply_markup=make_layer_keyboard())
    return DECOR


def get_decor(update: Update, cake_description):
    cake_description.bot_data['layer'] = update.message.text
    update.message.reply_text(text=static_text.select_decor, reply_markup=make_decor_keyboard())
    return TOPPING


def get_topping(update: Update, cake_description):
    cake_description.bot_data['decor'] = update.message.text
    update.message.reply_text(text=static_text.select_topping, reply_markup=make_topping_keyboard())
    return BERRIES


def get_berries(update: Update, cake_description):
    cake_description.bot_data['topping'] = update.message.text
    update.message.reply_text(text=static_text.select_berries, reply_markup=make_berries_keyboard())
    return CALCULATE


def calculate_order(update: Update, cake_description):
    cake_description.bot_data['berries'] = update.message.text
    print(cake_description.bot_data)
    shape = Shape.objects.get_or_create(name=f'{cake_description.bot_data["shape"]}')
    layer = Layer.objects.get_or_create(name=f'{cake_description.bot_data["layer"]}')
    decor = Decor.objects.get_or_create(name=f'{cake_description.bot_data["decor"]}')
    topping = Topping.objects.get_or_create(name=f'{cake_description.bot_data["topping"]}')
    berries = Berries.objects.get_or_create(name=f'{cake_description.bot_data["berries"]}')
    total_price = shape[0].price + layer[0].price + decor[0].price + topping[0].price + berries[0].price
    order_text = f'Итого Ваш заказ:\n' \
                 f'Форма торта - {cake_description.bot_data["shape"]}, цена {shape[0].price} ру.\n' \
                 f'Количество слоев - {cake_description.bot_data["layer"]}, цена {layer[0].price} ру.\n' \
                 f'Декор - {cake_description.bot_data["decor"]}, цена {decor[0].price} ру.\n' \
                 f'Топинг - {cake_description.bot_data["topping"]}, цена {topping[0].price} ру.\n' \
                 f'Ягоды - {cake_description.bot_data["berries"]}, цена {berries[0].price} ру.\n' \
                 f'Общая стоимость - {total_price} ру.'
    update.message.reply_text(text=order_text)
    update.message.reply_text(text=static_text.ordering)
    update.message.reply_text(text=static_text.address)
    return ORDER_CAKE


def command_cancel(update: Update, _):
    print('command_cancel')
    update.message.reply_text(text=static_text.cancel_text)
    return ConversationHandler.END


def get_order_for_cakes(update: Update, _):
    pass
    #TODO:Вызывается после выбора торта в меню заказа. Далее необходимо собрать адрес доставки, вычислить время заказа и указать время доставки. Может еще что забыл