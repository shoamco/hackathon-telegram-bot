import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater

import settings
from telegram import ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

import user_driver_bot

updater = Updater(token=settings.BOT_TOKEN, use_context=True)
logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

dispatcher = updater.dispatcher
from user_driver_bot import DRIVER_DATE, DRIVER_TIME, DRIVER_SOURCE, DRIVER_DESTINATION, DRIVER_PLACE

# start_handler = CommandHandler('start_driver', start)

driver_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start_driver', user_driver_bot.start_driver)],
    states={
        DRIVER_DATE: [MessageHandler(Filters.text, user_driver_bot.get_date)],
        DRIVER_TIME: [MessageHandler(Filters.text, user_driver_bot.get_time)],
        DRIVER_SOURCE: [MessageHandler(Filters.text, user_driver_bot.get_source)],
        DRIVER_DESTINATION: [MessageHandler(Filters.text, user_driver_bot.get_destination)],
        DRIVER_PLACE: [MessageHandler(Filters.text, user_driver_bot.get_place)]

    },

    fallbacks=[CommandHandler('cancel', user_driver_bot.cancel)]
)
dispatcher.add_handler(driver_conv_handler)

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
