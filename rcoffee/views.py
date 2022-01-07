import json
import logging
from django.http import HttpResponseForbidden, HttpResponse
import telebot
from django.views.decorators.csrf import csrf_exempt
from telebot import custom_filters
from DjangoCRUD import settings
from rcoffee.tg_views.tg_view import generate_tg_routes
from rcoffee.tg_views.welcome_view import WelcomeView


def index():
    return ''


@csrf_exempt
def webhook(request):
    if request.headers.get('content-type') == 'application/json':
        json_string = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return HttpResponse()
    else:
        return HttpResponseForbidden()


SMTP = False
ADMINS = settings.ADMINS

bot = telebot.TeleBot(settings.TG_BOT_TOKEN)
routes = generate_tg_routes(bot, default_view=WelcomeView)

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
