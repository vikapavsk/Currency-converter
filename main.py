import telebot
from telebot import types
from config import *
from extensions import Converter, APIException

conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard = True)
buttons = []
for val in exchanges.keys():
    buttons.append(types.KeyboardButton(val.capitalize()))

conv_markup.add(*buttons)


bot = telebot.TeleBot(TOKEN)  #инициализация объекта бота

@bot.message_handler(commands = ['start', 'help'])  #обработчик команд start/help
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: /convert \n Увидеть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])  #обработчик команды values
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in exchanges.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберите валюту, из которой хотите конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup = conv_markup)
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = 'Выберите валюту, в которую хотите конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup = conv_markup)
    bot.register_next_step_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
    sym = message.text.strip()
    text = 'Укажите количество конвертируемой валюты: '
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        new_price = Converter.get_price(base, sym, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка конвертации :\n{e}')
    else:
        text = f'Цена {amount} {base} в {sym} = {new_price}'
        bot.reply_to(message, text)

bot.polling()
