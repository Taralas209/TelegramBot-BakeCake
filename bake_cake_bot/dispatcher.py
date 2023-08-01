from telegram import Bot
from telegram.ext import (CommandHandler, ConversationHandler, Filters, MessageHandler, Updater, )
from bake_cake.settings import TELEGRAM_TOKEN
from bake_cake_bot.handlers import handlers


bot_handlers = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex('^(Авторизация)$'), handlers.get_auth_info),
    ],
    states={
        handlers.AUTH: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_auth_info)
        ],
        handlers.CREATE_USER: [
            MessageHandler(Filters.text & ~Filters.command, handlers.create_user)
        ],
        handlers.USER_PHONE: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_user_phone)
        ],
        handlers.MAIN_MENU: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_main_menu)
        ],
        handlers.ORDER: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_order)
        ],
        handlers.ORDER_CAKE: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_order_for_cakes)
        ],
        handlers.LAYER: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_layer)
        ],
        handlers.DECOR: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_decor)
        ],
        handlers.TOPPING: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_topping)
        ],
        handlers.BERRIES: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_berries)
        ],
        handlers.CALCULATE: [
            MessageHandler(Filters.text & ~Filters.command, handlers.calculate_order)
        ],
        handlers.PAY: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_pay)
        ],
        handlers.READY_ORDER: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_order_for_ready_cakes)
        ],
    },
    fallbacks=[
        CommandHandler("cancel", handlers.command_cancel)
    ]
)


def setup_dispatcher(dp):
    dp.add_handler(bot_handlers)
    dp.add_handler(CommandHandler("start", handlers.command_start))
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
