from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from . import static_text
from bake_cake_bot.models import Users
from .keyboard_utils import make_keyboard_for_start_command, make_main_menu_keyboard


AUTH, CREATE_USER, USER_PHONE, MAIN_MENU = range(4)


def command_start(update: Update, context):
    print('command_start')
    if update.message:
        user_info = update.message.from_user.to_dict()
    else:
        user_info = {'id': context.user_data['user_id'], 'username': context.user_data['username'],
                     'first_name': context.user_data['first_name']}

    user, created = Users.objects.get_or_create(telegram_id=user_info['id'], username=user_info['username'])

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
        update.message.reply_text(text='ТУТ БУДЕТ МЕНЮ ЗАКАЗА')
        return MAIN_MENU
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


def command_cancel(update: Update, _):
    print('command_cancel')
    update.message.reply_text(text=static_text.cancel_text)
    return ConversationHandler.END
