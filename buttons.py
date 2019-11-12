from pymongo import MongoClient
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import date, timedelta
client = MongoClient()


def to_cols(data, n_cols=2):
    menu, row = [], []
    for x in data:
        if len(row) == n_cols:
            menu.append(row)
            row = []
        row.append(x)
    if row:
        menu.append(row)
    return menu


def get_enter_buttons():
    buttons = [InlineKeyboardButton(s, callback_data=s[:64]) for s in ['Offer a trip', 'Search a trip']]
    reply_markup = InlineKeyboardMarkup(to_cols(buttons))
    return reply_markup


def get_dates_options():
    days = [date.today() + timedelta(days=i) for i in range(3)]
    buttons = [InlineKeyboardButton(f"{day}", callback_data=f"{day}") for day in days]
    reply_markup = InlineKeyboardMarkup(to_cols(buttons, 3))
    return reply_markup


def get_collection_buttons(collection):
    """db = client.get_database("trempDB")
    trips = db.get_collection("trips")
    collection = trips.find({})"""
    buttons = []
    for item in collection:
        data = f"{item['name']} :"
        buttons.append(InlineKeyboardButton(data, callback_data=f"{item['_id']}", kwargs={'driverID': {item['_id']}}))

    reply_markup = InlineKeyboardMarkup(to_cols(buttons, 1))
    return reply_markup