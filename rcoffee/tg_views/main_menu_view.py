from typing import Optional

from telebot import types

from rcoffee.orm import set_field
from django.utils.translation import gettext as _
from rcoffee.tg_views.tg_view import TgView


class MainMenuView(TgView):
    def onStart(self):
        self.bot.send_message(
            self.user_id, _('Main menu'), reply_markup=self.keyboard())

    def keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 1

        keyboard.add(
            types.InlineKeyboardButton(
                text=_('Show profile'),
                callback_data='change_name'
            ),
            types.InlineKeyboardButton(
                text=_('Change profile'),
                callback_data='change_link'
            ),
            types.InlineKeyboardButton(
                text=_('My teams'),
                callback_data='change_work'
            ),
            types.InlineKeyboardButton(
                text=_('Status'),
                callback_data='change_about'
            ),
            types.InlineKeyboardButton(
                text=_('Back'),
                callback_data='back'
            )
        )
        return keyboard
