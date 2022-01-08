from typing import Optional

from telebot import types

from rcoffee.orm import set_field
from django.utils.translation import gettext as _
from rcoffee.tg_views.tg_view import TgView


class MainMenuView(TgView):
    def onStart(self):
        self.bot.send_message(self.user_id, 'Menu')
