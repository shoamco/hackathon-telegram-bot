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

updater = Updater(token=settings.BOT_TOKEN, use_context=True)
logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

dispatcher = updater.dispatcher
from user_driver_bot import DRIVER_DATE, DRIVER_TIME, DRIVER_SOURCE, DRIVER_DESTINATION, DRIVER_PLACE
from usre_passenger_bot import PASSENGER_CONFIRMATION_RIDE

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


def get_phone(update, context):
    chat_id = update.effective_chat.id
    phone = update.message.contact.phone_number
    logger.info(f"get_phone#{chat_id} phone {phone}")
    context.user_data['phone'] = phone

    update.message.reply_text(text="Are you a passenger or a driver? ",
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
        PHONE: [MessageHandler(Filters.contact, get_phone, edited_updates=True)]

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
    entry_points=[CommandHandler('passenger', usre_passenger_bot.select_ride)],
    states={

        PASSENGER_CONFIRMATION_RIDE: [CallbackQueryHandler(usre_passenger_bot.confirmation_ride)]

    },

    fallbacks=[CommandHandler('cancel', user_driver_bot.cancel)]
)
dispatcher.add_handler(passenger_conv_handler)
logger.info("* Start polling...")

updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
