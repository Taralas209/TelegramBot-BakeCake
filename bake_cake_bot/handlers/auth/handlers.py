from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from bake_cake_bot.handlers.auth import static_text
from bake_cake_bot.models import Users
from .keyboard_utils import make_keyboard_for_start_command


AUTH_INFO, START_BOT = range(2)


def command_start(update: Update, context):
    print('command_start')
    if update.message:
        user_info = update.message.from_user.to_dict()
    else:
        user_info = {'id': context.user_data['user_id'], 'username': context.user_data['username'],
                     'first_name': context.user_data['first_name']}
    user, created = Users.objects.get_or_create(
        telegram_id=user_info['id'],
        username=user_info['username'],
    )

    if created:
        text = static_text.start_created.format(
            first_name=user_info['first_name']
        )
    else:
        text = static_text.start_not_created.format(
            first_name=user_info['first_name']
        )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=make_keyboard_for_start_command(),
    )


def get_auth_info(update: Update, _):

    return AUTH_INFO

