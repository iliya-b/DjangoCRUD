from typing import Optional

from telebot import types

from rcoffee.orm import set_field
from django.utils.translation import gettext as _
from rcoffee.tg_views.tg_view import TgView


class ShowStatusView(TgView):

    @staticmethod
    def callbacks():
        return {
            'back': ShowStatusView.back
        }

    def back(self):
        print('back')

    def onStart(self):
        self.bot.send_message(
            self.user_id, _('Your profile'), reply_markup=self.keyboard())

    def keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 1

        keyboard.add(
            types.InlineKeyboardButton(
                text=_('Back'),
                callback_data='back'
            )
        )
        return keyboard
