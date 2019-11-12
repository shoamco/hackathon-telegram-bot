import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater

import settings
from telegram import ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
DRIVER_DATE, DRIVER_TIME, DRIVER_SOURCE, DRIVER_DESTINATION, DRIVER_PLACE = range(5)
logger = logging.getLogger(__name__)
def start_driver(update, context):
    chat_id = update.effective_chat.id
    logger.info(f"in start_driver #{chat_id}")
    update.message.reply_text('Enter a travel date\n', one_time_keyboard=True)
    context.user_data['driver'] = dict()
    return DRIVER_DATE

def get_date(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_date #{chat_id}")
    context.user_data['driver']['date'] = text

    update.message.reply_text('At what time do you want to leave?')


    return DRIVER_TIME

def get_time(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_time #{chat_id}")
    context.user_data['driver']['time'] = text

    update.message.reply_text('Enter place of departure:')

    return DRIVER_SOURCE





def get_source(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_source #{chat_id}")
    context.user_data['driver']['source'] = text

    update.message.reply_text('Enter a destination :')

    return DRIVER_DESTINATION


def get_destination(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_destination #{chat_id}")
    context.user_data['driver']['destination'] = text

    update.message.reply_text(' How many spare places do you have?')
    return DRIVER_PLACE


def get_place(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"in get_place #{chat_id}")
    context.user_data['driver']['place'] = text

    update.message.reply_text(f"Your ride has been recorded:\n"
                              f"{context.user_data['driver']}")
    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
