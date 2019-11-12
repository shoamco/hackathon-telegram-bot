"""import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater
import buttons
import settings
from telegram import ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

import logging

from telegram import Update, CallbackQuery
from telegram.ext import CommandHandler, CallbackContext

logger = logging.getLogger(__name__)
PASSENGER_CONFIRMATION_RIDE = range(2)


def select_ride(update, context):
    chat_id = update.effective_chat.id
    logger.info(f"Passenger:in select_ride #{chat_id}")
    update.message.reply_text('Please select a ride:\n', one_time_keyboard=True,
                              reply_markup=buttons.get_dates_options())
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
"""

#===========================================================================
#                      SHOAM UPDATES
#===========================================================================

import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater
import buttons
import settings
from telegram import ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

import logging

from telegram import Update, CallbackQuery
from telegram.ext import CommandHandler, CallbackContext

from db_functions import get_source_destination_list

logger = logging.getLogger(__name__)
PASSENGER_DATE, PASSENGER_TIME, PASSENGER_SOURCE, PASSENGER_DESTINATION, PASSENGER_PLACE, PASSENGER_SELECT_RIDE, PASSENGER_CONFIRMATION_RIDE = range(
    7)
import library_functions


def start_passenger(update, context):
    chat_id = update.effective_chat.id
    logger.info(f"! PASSENGER start_passenger[#{chat_id}] .")
    update.message.reply_text('Enter a travel date\n', one_time_keyboard=True, reply_markup=buttons.get_dates_options())
    context.user_data['ride'] = dict()
    # context.user_data['user'] = {"id": chat_id, "first_name": first_name, "last_name": last_name, "username": username}
    return PASSENGER_DATE


def get_date(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    query: CallbackQuery = update.callback_query

    text = query.data

    logger.info(f"! PASSENGER [#{chat_id}] Callback {text!r}.")
    logger.info(f"in get_date #{chat_id}")
    context.user_data['ride']['date'] = text

    context.bot.send_message(chat_id=chat_id, text='At what time do you need to leave?', reply_markup=None)

    return PASSENGER_TIME


def get_time(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_time #{chat_id} text{text}")
    logger.info(f"time {text}, {library_functions.validation_hour(text)}")

    if not library_functions.validation_hour(text):  # if time is invalid
        update.message.reply_text('invalid time, please enter again?')
        return PASSENGER_TIME

    update.message.reply_text('Enter place of departure:')
    context.user_data['ride']['time'] = text
    return PASSENGER_SOURCE


def get_source(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_source #{chat_id}")

    if not library_functions.place_validation(text):
        update.message.reply_text(' invalid name place, please enter again?')
        return PASSENGER_SOURCE
    context.user_data['ride']['source'] = text
    update.message.reply_text('Enter a destination :')

    return PASSENGER_DESTINATION


def get_destination(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_destination #{chat_id} text{text}")

    if not library_functions.place_validation(text):
        update.message.reply_text(' invalid name place, please enter again?')
        return PASSENGER_SOURCE

    context.user_data['ride']['destination'] = text
    update.message.reply_text(' How many  places do you need?')
    return PASSENGER_PLACE


def get_place(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_place #{chat_id}")
    context.user_data['ride']['place'] = text

    chat_id = update.effective_chat.id
    logger.info(f"Passenger:in select_ride #{chat_id}")
    trips = library_functions.get_trips(context.user_data['ride'])
    update.message.reply_text('Please select a ride:\n', one_time_keyboard=True, reply_markup=buttons.get_collection_buttons(trips))

    return PASSENGER_SELECT_RIDE




def select_ride(update, context):
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