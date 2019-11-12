import logging
from ctypes import util

from telegram import Update, CallbackQuery
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater, CallbackQueryHandler
import settings
# YOUR BOT HERE
logging.basicConfig(format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
updater = Updater(token=settings.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher



updater = Updater(token=settings.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.contact, ))
dispatcher.add_handler(CallbackQueryHandler())
dispatcher.add_handler(CommandHandler('start', ))
logger.info("* Start polling")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Stops until Ctrl+C is pressed
logger.info("* Bye!")