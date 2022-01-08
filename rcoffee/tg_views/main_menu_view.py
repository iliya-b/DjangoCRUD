from typing import Optional

from telebot import types

from rcoffee.orm import set_field
from django.utils.translation import gettext as _
from rcoffee.tg_views.tg_view import TgView
from rcoffee.tg_views.show_profile_view import ShowProfileView
from rcoffee.tg_views.change_profile_view import ChangeProfileView
from rcoffee.tg_views.change_teams_view import ChangeTeamsView
from rcoffee.tg_views.show_status_view import ShowStatusView


class MainMenuView(TgView):

    @staticmethod
    def callbacks():
        return {
            'show_profile': ShowProfileView.onStart,
            'change_profile': ChangeProfileView.onStart,
            'show_teams': ChangeTeamsView.onStart,
            'show_status': ShowStatusView.onStart,
            'back': MainMenuView.back
        }

    def back(self):
        print('back')

    def onStart(self):
        self.bot.send_message(
            self.user_id, _('Main menu'), reply_markup=self.keyboard())

    def keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 1

        keyboard.add(
            types.InlineKeyboardButton(
                text=_('Show profile'),
                callback_data='show_profile'
            ),
            types.InlineKeyboardButton(
                text=_('Change profile'),
                callback_data='change_profile'
            ),
            types.InlineKeyboardButton(
                text=_('My teams'),
                callback_data='change_teams'
            ),
            types.InlineKeyboardButton(
                text=_('Status'),
                callback_data='show_status'
            ),
            types.InlineKeyboardButton(
                text=_('Back'),
                callback_data='back'
            )
        )
        return keyboard
