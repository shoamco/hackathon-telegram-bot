import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater

import settings
from telegram import ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)

import user_driver_bot
import buttons
updater = Updater(token=settings.BOT_TOKEN, use_context=True)
logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

dispatcher = updater.dispatcher
from user_driver_bot import DRIVER_DATE, DRIVER_TIME, DRIVER_SOURCE, DRIVER_DESTINATION, DRIVER_PLACE

# start_handler = CommandHandler('start_driver', start)
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    # context.bot.send_message(chat_id=chat_id, text=" Welcome\nAre you a passenger or a driver? ",reply_markup=buttons.get_enter_buttons())
    update.message.reply_text( text=" Welcome\nAre you a passenger or a driver? ",
                              reply_markup=buttons.get_enter_buttons())
    logger.info(f"> afeter #{chat_id}")


start_handler = CommandHandler(['start'], start)
dispatcher.add_handler(start_handler)
driver_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('driver', user_driver_bot.start_driver)],
    states={
        # DRIVER_DATE: [MessageHandler(Filters.text, user_driver_bot.get_date)],
        DRIVER_DATE: [CallbackQueryHandler(user_driver_bot.get_date)],
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
