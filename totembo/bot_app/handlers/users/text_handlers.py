from telebot.types import Message

from store.models import Category, Product
from ...keyboards import *
from ...loader import bot

@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    categories = [item.title for item in Category.objects.filter(parent=None)]
    bot.send_message(chat_id, 'Sa\'lem!', reply_markup=get_rep_btn(categories))

@bot.message_handler(func=lambda message: message.text in [item.title for item in Category.objects.filter(parent=None)])
def reaction_categories(message: Message):
    chat_id = message.chat.id
    category = Category.objects.get(title=message.text)
    subcategories = [item.title for item in Category.objects.filter(parent=category)]
    subcategories.append('Artqa qaytiw!')
    bot.send_message(chat_id, category.title, reply_markup=get_rep_btn(subcategories))

@bot.message_handler(func=lambda message: message.text == 'Artqa qaytiw!')
def reaction_back_categories(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Kategoriyalar:', reply_markup=get_rep_btn([item.title for item in Category.objects.filter(parent=None)]))

@bot.message_handler(func=lambda message: message.text in [item.title for item in Category.objects.filter(parent=True)])
def reaction_subcategories(message: Message):
    chat_id = message.chat.id
    subcategory = Category.objects.get(title=message.text)
    products = Product.objects.filter(category=subcategory)
    bot.send_message(chat_id, 'Products', reply_markup=get_rep_btn([item.title for item in products]))


@bot.message_handler(func=lambda message: message.text in [item.title for item in Product.objects.all()])
def reaction_product(message: Message):
    chat_id = message.chat.id
    product = Product.objects.get(title=message.text)
    bot.send_message(chat_id, product, reply_markup=get_rep_btn([item.title for item in Product.objects.all()]))




