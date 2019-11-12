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

"""
def get_collection_buttons(collection, key_field='_id'):
    db = client.get_database("my_school")
    trips = db.get_collection("students")
    collection = trips.find({})
    buttons = []
    for element in collection:
        data = ''
        for key, value in element.item():
            data += f"{key} : {value} \n"
            buttons.append(InlineKeyboardButton(data, callback_data=f"{element[key_field]}"))
    reply_markup = InlineKeyboardMarkup(to_cols(buttons, 1))
    return reply_markup"""


def get_collection_buttons(collection,keys_to_fetch =[],key_field=None):
    if key_field is None: key_field = '_id'
    buttons = []
    for element in collection:
        data = ''
        assert (isinstance(element, dict))
        for key in element.keys():
            if key == "_id" : continue
            data += f"{key} : {element[key]} \n"
        buttons.append(InlineKeyboardButton(data, callback_data=f"{element[key_field]}"))
    reply_markup = InlineKeyboardMarkup(to_cols(buttons, 1))
    return reply_markup