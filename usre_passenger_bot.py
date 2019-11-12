
import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater
import buttons
import settings
from telegram import ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)


import logging

from telegram import Update,CallbackQuery
from telegram.ext import CommandHandler, CallbackContext

DRIVER_DATE, DRIVER_TIME, DRIVER_SOURCE, DRIVER_DESTINATION, DRIVER_PLACE = range(5)
logger = logging.getLogger(__name__)

def select_ride(update, context):
    chat_id = update.effective_chat.id
    logger.info(f"in select_ride #{chat_id}")
    update.message.reply_text('Please select a ride:\n', one_time_keyboard=True, reply_markup=buttons.get_dates_options())
