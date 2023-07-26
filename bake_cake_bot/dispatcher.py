import logging
import sys

import telegram.error
from telegram import Bot
from telegram.ext import (CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, Updater,
                          CallbackQueryHandler, ShippingQueryHandler)
from bake_cake.settings import DEBUG, TELEGRAM_TOKEN
from bake_cake_bot.handlers.admin import handlers as admin_handlers
from bake_cake_bot.handlers.customer import handlers as customer_handlers


meetup_handlers = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex('^(Выход)$'),
                       admin_handlers.exit),
    ],
    states={
        customer_handlers.OPTION: [
            MessageHandler(Filters.text & ~Filters.command, customer_handlers.choose_admin_button)
        ],

    },
    fallbacks=[
        CommandHandler("cancel", customer_handlers.command_cancel)
    ]
)


def setup_dispatcher(dp):
    dp.add_handler(meetup_handlers)

    dp.add_handler(CommandHandler("start", customer_handlers.command_start))
    dp.add_handler(CommandHandler("cancel", customer_handlers.command_cancel))

    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f'https://t.me/{bot_info["username"]}'

    print(f"Pooling of '{bot_link}' started")

    updater.start_polling()
    updater.idle()


bot = Bot(TELEGRAM_TOKEN)
try:
    TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
except telegram.error.Unauthorized:
    logging.error(f"Invalid TELEGRAM_TOKEN.")
    sys.exit(1)

n_workers = 1 if DEBUG else 4
dispatcher = setup_dispatcher(
    Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True)
)
