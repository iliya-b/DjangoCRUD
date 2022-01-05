import time

import telebot
from django.core.management.base import BaseCommand

from DjangoCRUD import settings


class Command(BaseCommand):
    help = 'Updates webhook'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TG_BOT_TOKEN)
        bot.remove_webhook()
        time.sleep(0.1)
        bot.set_webhook(url=settings.BASE_URL + '/rcoffee/webhook/')
        self.stdout.write(self.style.SUCCESS('webhook set'))
