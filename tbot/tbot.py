import telebot

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import types

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)


def set_webhook(request):
    webhook_address = settings.TELEGRAM_BOT_WEBHOOK_URL
    bot.remove_webhook()
    bot.set_webhook(webhook_address)
    return HttpResponse(
        f'<h1>set_webhook---> {settings.TELEGRAM_BOT_WEBHOOK_URL}</h1>')


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])
    return HttpResponse('<h1>Bot live!</h1>')


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):

    # menu
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Info")
    item2 = types.KeyboardButton("send point", request_location=True)
    markup.row(item1, item2)

    bot.send_message(message.chat.id, 'Нажми на кнопку получишь результат', reply_markup=markup)


# # send point
# @bot.message_handler(func=lambda message: message.text == "send point")
# def shedule(message):
#
#
#
#
#     bot.reply_to(message, 'send point')



@bot.message_handler(content_types=['location'])
def echo_message(message):
    chat_id = message.chat.id
    latitude = message.location.latitude
    longitude = message.location.longitude

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Добавить описание', callback_data=f'setcity:{12312}')
    button2 = types.InlineKeyboardButton('Добавить фото', callback_data=f'setcity:{12312}')
    markup.add(button1, button2)

    bot.send_message(chat_id, f'lat: {latitude}\nlon: {longitude}', reply_markup=markup)


