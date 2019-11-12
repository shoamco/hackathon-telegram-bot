import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater
from telegram import InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
import settings
import usre_passenger_bot
from telegram import ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)

import user_driver_bot
import buttons
from telegram import ReplyKeyboardRemove, KeyboardButton
import library_functions

updater = Updater(token=settings.BOT_TOKEN, use_context=True)
logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

dispatcher = updater.dispatcher
from user_driver_bot import DRIVER_DATE, DRIVER_TIME, DRIVER_SOURCE, DRIVER_DESTINATION, DRIVER_PLACE
from usre_passenger_bot import PASSENGER_DATE, PASSENGER_TIME, PASSENGER_SOURCE, PASSENGER_DESTINATION, PASSENGER_PLACE, \
    PASSENGER_SELECT_RIDE,PASSENGER_CONFIRMATION_RIDE

PHONE = range(1)


# start_handler = CommandHandler('start_driver', start)
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat select passenger/driver #{chat_id}")

    contact_keyboard = KeyboardButton(text="send_contact", request_contact=True)
    custom_keyboard = [[contact_keyboard]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=chat_id,
                             text=" Welcome\nWould you mind sharing your location and contact with me?",
                             reply_markup=reply_markup)

    logger.info(f"> after #{chat_id}")
    return PHONE


def get_data_user(update, context):
    chat_id = update.effective_chat.id
    phone = update.message.contact.phone_number
    logger.info(f"get_phone#{chat_id} phone {phone}")

    chat_id = update.effective_chat.id
    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name
    username = update.effective_chat.username
    context.user_data['user'] = {"id": chat_id, "first_name": first_name, "last_name": last_name, "username": username,
                                 "phone": phone}

    library_functions.insert_user(context.user_data['user'])

    update.message.reply_text(text=f"user:{context.user_data['user']}\n Are you a passenger or a driver? ",
                              reply_markup=buttons.get_enter_buttons())

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('cancel.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def get_type_user():
    pass


def debug(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"in debug #{chat_id}")
    update.message.reply_text(text="all the details ")


#
# start_handler = CommandHandler(['start'], start)
# dispatcher.add_handler(start_handler)

debug_handler = CommandHandler(['debug'], debug)
dispatcher.add_handler(debug_handler)

# passenger_handler = CommandHandler(['passenger'], usre_passenger_bot.select_ride)
# dispatcher.add_handler(passenger_handler)
start_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        PHONE: [MessageHandler(Filters.contact, get_data_user, edited_updates=True)]

    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
dispatcher.add_handler(start_conv_handler)

driver_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('driver', user_driver_bot.start_driver)],
    states={

        DRIVER_DATE: [CallbackQueryHandler(user_driver_bot.get_date)],
        DRIVER_TIME: [MessageHandler(Filters.text, user_driver_bot.get_time)],
        DRIVER_SOURCE: [MessageHandler(Filters.text, user_driver_bot.get_source)],
        DRIVER_DESTINATION: [MessageHandler(Filters.text, user_driver_bot.get_destination)],
        DRIVER_PLACE: [MessageHandler(Filters.text, user_driver_bot.get_place)]

    },

    fallbacks=[CommandHandler('cancel', user_driver_bot.cancel)]
)
dispatcher.add_handler(driver_conv_handler)

passenger_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('passenger', usre_passenger_bot.start_passenger)],
    states={


        PASSENGER_DATE: [CallbackQueryHandler(usre_passenger_bot.get_date)],
        PASSENGER_TIME: [MessageHandler(Filters.text, usre_passenger_bot.get_time)],
        PASSENGER_SOURCE: [MessageHandler(Filters.text, usre_passenger_bot.get_source)],
        PASSENGER_DESTINATION: [MessageHandler(Filters.text, usre_passenger_bot.get_destination)],
        PASSENGER_PLACE: [MessageHandler(Filters.text, usre_passenger_bot.get_place)],
        PASSENGER_SELECT_RIDE: [CallbackQueryHandler(usre_passenger_bot.select_ride)]


    },

    fallbacks=[CommandHandler('cancel', user_driver_bot.cancel)]
)
dispatcher.add_handler(passenger_conv_handler)
logger.info("* Start polling...")

updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
