import logging
import sys

import telegram.error
from telegram import Bot
from telegram.ext import (CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, Updater,
                          CallbackQueryHandler, ShippingQueryHandler)
from bake_cake.settings import TELEGRAM_TOKEN
from bake_cake_bot.handlers.auth import handlers as auth_handlers
from bake_cake_bot.handlers.admin import handlers as admin_handlers
from bake_cake_bot.handlers.customer import handlers as customer_handlers


meetup_handlers = ConversationHandler(
    entry_points=[
        # MessageHandler(Filters.regex('^(Авторизация)$'),
        #                auth_handlers.auth),

    ],
    states={
        auth_handlers.AUTH_INFO: [
            MessageHandler(Filters.text & ~Filters.command, auth_handlers.get_auth_info)
        ],

    },
    fallbacks=[
        CommandHandler("cancel", customer_handlers.command_cancel)
    ]
)


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher.add_handler(CommandHandler("start", auth_handlers.command_start))

    bot_info = Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f'https://t.me/{bot_info["username"]}'

    print(f"Pooling of '{bot_link}' started")

    updater.start_polling()
    updater.idle()
