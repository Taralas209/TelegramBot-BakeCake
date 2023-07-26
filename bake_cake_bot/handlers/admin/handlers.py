from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from bake_cake_bot.handlers.admin import static_text
from bake_cake_bot.models import Users
from .keyboard_utils import make_keyboard_with_admin_features


def command_admin(update: Update, _):
    pass

