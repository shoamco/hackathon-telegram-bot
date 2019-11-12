"""import logging
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater
import buttons
import settings
import library_functions
from telegram import ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

import logging

from telegram import Update, CallbackQuery
from telegram.ext import CommandHandler, CallbackContext
import library_functions

DRIVER_DATE, DRIVER_TIME, DRIVER_SOURCE, DRIVER_DESTINATION, DRIVER_PLACE = range(5)
logger = logging.getLogger(__name__)


def start_driver(update, context):
    chat_id = update.effective_chat.id
    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name
    username = update.effective_chat.username
    logger.info(f"in start_driver id#{chat_id} name {first_name} {last_name} username {username}")
    update.message.reply_text('Enter a travel date\n', one_time_keyboard=True, reply_markup=buttons.get_dates_options())
    context.user_data['ride'] = dict()
    context.user_data['user'] = {"id": chat_id, "first_name": first_name, "last_name": last_name, "username": username}
    return DRIVER_DATE


def get_date(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    query: CallbackQuery = update.callback_query

    text = query.data
    # text = update.message.text
    # chat_id = update.effective_chat.id
    logger.info(f"! [#{chat_id}] Callback {text!r}.  Checking age...")
    logger.info(f"in get_date #{chat_id}")
    context.user_data['ride']['date'] = text

    context.bot.send_message(chat_id=chat_id, text='At what time do you want to leave?', reply_markup=None)

    return DRIVER_TIME


def get_time(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_time #{chat_id} text{text}")
    logger.info(f"time {text}, {library_functions.validation_hour(text)}")

    if not library_functions.validation_hour(text):  # if time is invalid
        update.message.reply_text('invalid time, please enter again?')
        return DRIVER_TIME

    update.message.reply_text('Enter place of departure:')
    context.user_data['ride']['time'] = text
    return DRIVER_SOURCE


def get_source(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_source #{chat_id}")

    if not library_functions.place_validation(text):
        update.message.reply_text(' invalid name place, please enter again?')
        return DRIVER_SOURCE
    context.user_data['ride']['source'] = text
    update.message.reply_text('Enter a destination :')

    return DRIVER_DESTINATION


def get_destination(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_destination #{chat_id} text{text}")

    if not library_functions.place_validation(text):
        update.message.reply_text(' invalid name place, please enter again?')
        return DRIVER_SOURCE

    context.user_data['ride']['destination'] = text
    update.message.reply_text(' How many spare places do you have?')
    return DRIVER_PLACE


def get_place(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_place #{chat_id}")
    context.user_data['ride']['place'] = text

    update.message.reply_text(f"Your ride has been recorded:\n"
                              f"ride: {context.user_data['ride']}\n"
                              f"user:{context.user_data['user']} ")
    library_functions.insert_ride_to_db(context.user_data['ride'], chat_id)
    library_functions.insert_user(context.user_data['user'])
    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user,
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('cancel.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
"""


#===========================================================================
#                      SHOAM UPDATES
#===========================================================================
import logging

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater
import buttons
import settings
import library_functions
from telegram import ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

import logging

from telegram import Update, CallbackQuery
from telegram.ext import CommandHandler, CallbackContext
import library_functions

DRIVER_DATE, DRIVER_TIME, DRIVER_SOURCE, DRIVER_DESTINATION, DRIVER_PLACE = range(5)
logger = logging.getLogger(__name__)


def start_driver(update, context):
    chat_id = update.effective_chat.id

    update.message.reply_text('Enter a travel date\n', one_time_keyboard=True, reply_markup=buttons.get_dates_options())
    context.user_data['ride'] = dict()
    # context.user_data['user'] = {"id": chat_id, "first_name": first_name, "last_name": last_name, "username": username}
    return DRIVER_DATE





def get_date(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    query: CallbackQuery = update.callback_query

    text = query.data
    # text = update.message.text
    # chat_id = update.effective_chat.id
    logger.info(f"! [#{chat_id}] Callback {text!r}")
    logger.info(f"in get_date #{chat_id}")
    context.user_data['ride']['date'] = text

    context.bot.send_message(chat_id=chat_id, text='At what time do you want to leave?', reply_markup=None)

    return DRIVER_TIME


def get_time(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_time #{chat_id} text{text}")
    logger.info(f"time {text}, {library_functions.validation_hour(text)}")

    if not library_functions.validation_hour(text):  # if time is invalid
        update.message.reply_text('invalid time, please enter again?')
        return DRIVER_TIME

    update.message.reply_text('Enter place of departure:')
    context.user_data['ride']['time'] = text
    return DRIVER_SOURCE


def get_source(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_source #{chat_id}")

    if not library_functions.place_validation(text):
        update.message.reply_text(' invalid name place, please enter again?')
        return DRIVER_SOURCE
    context.user_data['ride']['source'] = text
    update.message.reply_text('Enter a destination :')

    return DRIVER_DESTINATION


def get_destination(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_destination #{chat_id} text{text}")

    if not library_functions.place_validation(text):
        update.message.reply_text(' invalid name place, please enter again?')
        return DRIVER_SOURCE

    context.user_data['ride']['destination'] = text
    update.message.reply_text(' How many spare places do you have?')
    return DRIVER_PLACE


def get_place(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_place #{chat_id}")
    context.user_data['ride']['place'] = text

    update.message.reply_text(f"Your ride has been recorded:\n"
                              f"ride: {context.user_data['ride']}\n")
    library_functions.insert_ride_to_db(context.user_data['ride'], chat_id)

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('cancel.', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END