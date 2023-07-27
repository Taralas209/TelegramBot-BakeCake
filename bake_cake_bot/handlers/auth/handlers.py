from telegram import Update
from telegram.ext import ConversationHandler

from bake_cake_bot.handlers.auth import static_text
from bake_cake_bot.models import Users
from .keyboard_utils import make_keyboard_for_start_command

CREATE_USER, USER_PHONE = range(2)


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


def get_auth_info(update: Update, _):
    auth = update.message.text
    if auth == static_text.start_button_text[0]:
        print('Auth pressed')
        user_info = update.message.from_user.to_dict()
        user = Users.objects.get(telegram_id=user_info['id'])
        if not user.phone:
            print('registration_request')
            update.message.reply_text(static_text.need_auth)
            #TODO отправка файла соглашения о конфиленциальности в txt
            text = static_text.name
            update.message.reply_text(
                text=text
            )
            return CREATE_USER
        else:
            if user.is_admin:
                print('admin detected')
                # TODO переход к меню админа
                return ConversationHandler.END
            else:
                print('customer detected')
                # TODO переход в меню заказчика
                return ConversationHandler.END


def create_user(update: Update, user_description):
    print('create_user, get name')
    user_description.bot_data['name'] = update.message.text
    text = static_text.phone
    update.message.reply_text(
        text=text
    )
    return USER_PHONE


def get_user_phone(update: Update, user_description):
    print('create_user, get phone')
    user_description.bot_data['phone'] = update.message.text
    user_info = update.message.from_user.to_dict()
    user = Users.objects.get(telegram_id=user_info['id'])
    user.name = user_description.bot_data['name']
    user.phone = user_description.bot_data['phone']
    user.save()
    text = static_text.user_saved
    update.message.reply_text(
        text=text
    )
    return ConversationHandler.END
