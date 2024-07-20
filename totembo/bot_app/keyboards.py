from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_rep_btn(lst: list):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for item in lst:
        markup.add(KeyboardButton(item))
    return markup