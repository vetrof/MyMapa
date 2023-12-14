import telebot
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import types

from tbot.models import Places

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

    bot.send_message(message.chat.id, 'Нажми на кнопку получишь результат',
                     reply_markup=markup)


@bot.message_handler(content_types=['location'])
def echo_message(message):
    chat_id = message.chat.id
    lat_decimal = message.location.latitude
    lon_decimal = message.location.longitude
    link_to_google_map = \
        (f"[Open in google map](https://www.google.com/maps/place/"
         f"{lat_decimal}+{lon_decimal})")

    new_place = Places(
        tg_user_id=1,longitude=lat_decimal,latitude=lon_decimal
    )
    new_place.save()
    place_id = new_place.id

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        'Добавить описание', callback_data=f'info {place_id}'
    )
    button2 = types.InlineKeyboardButton(
        'Добавить фото', callback_data=f'foto {place_id}'
    )
    markup.add(button1, button2)

    bot.send_message(
        chat_id,
        f'{lat_decimal} {lon_decimal}\n{link_to_google_map}'
        f'\nplace id:{place_id}',
        parse_mode='Markdown',
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('info'))
def callback_set_city(call):
    # Получаем place_id из callback_data
    place_id = call.data.split()[1]

    # Ожидаем следующее сообщение пользователя
    bot.send_message(
        call.message.chat.id, 'Введите описание ниже:'
    )
    bot.register_next_step_handler(
        call.message,
        process_description_input,
        place_id
    )


def process_description_input(message, place_id):

    place = Places.objects.get(id=place_id)
    place.note = message.text
    place.save()

    bot.send_message(
        message.chat.id,
        f'Описание сохранено: {message.text} {place_id}'
    )
