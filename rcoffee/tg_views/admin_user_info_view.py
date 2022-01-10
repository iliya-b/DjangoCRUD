from typing import Optional

from telebot import types

from rcoffee.models import User
from rcoffee.orm import set_field, get_user
from django.utils.translation import gettext as _
from rcoffee.tg_views.tg_view import TgView


class AdminUserInfoView(TgView):

    @staticmethod
    def callbacks():
        return {
            'back': AdminUserInfoView.back
        }

    def back(self, message):
        print('back')

    def onStart(self):
        user = User.objects.get(pk=self.args['user_id'])
        self.bot.send_message(
            self.user_id, _('Profile') + str(user), reply_markup=self.keyboard()
        )

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
