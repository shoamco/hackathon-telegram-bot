
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


logger = logging.getLogger(__name__)
PASSENGER_CONFIRMATION_RIDE = range(2)
def select_ride(update, context):
    chat_id = update.effective_chat.id
    logger.info(f"Passenger:in select_ride #{chat_id}")
    update.message.reply_text('Please select a ride:\n', one_time_keyboard=True, reply_markup=buttons.get_dates_options())
    return PASSENGER_CONFIRMATION_RIDE

def confirmation_ride(update, context):
    chat_id = update.effective_chat.id
    chat_id = update.effective_chat.id
    query: CallbackQuery = update.callback_query

    text = query.data
    logger.info(f"Passenger:Confirmation_trip #{chat_id}")

    context.bot.send_message(chat_id=chat_id, text=f"You travel with:\n {text}", reply_markup=None)
    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("passenger %s canceled the conversation.", user.first_name)
    update.message.reply_text('cancel. passenger',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END