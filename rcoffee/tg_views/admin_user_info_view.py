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
        from rcoffee.tg_views.admin_menu_view import AdminMenuView
        self.change_view(AdminMenuView, {'base_message': message.id})

    def _user_info(self, user):
        self.bot.send_message(
            self.user_id, _('Profile') + str(user), reply_markup=self.keyboard()
        )

    def onStart(self):
        if 'user_id' in self.args:
            self._user_info(User.objects.get(pk=self.args['user_id']))
        else:
            self.bot.edit_message_text(
                _('Enter user id or name'), self.user_id, self.args['base_message']
            )

    def onMessage(self, message):
        admin = get_user(self.user_id)
        try:
            id = int(message.text)
        except ValueError:
            return
        user = User.objects.get(telegram_id=id, teams__admin_id__in=[admin.id])
        if user:
            self.args['user_id'] = user.id

        self.onStart()

    def keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 1

        keyboard.add(
            types.InlineKeyboardButton(
                text=_('< Back'),
                callback_data='back'
            )
        )
        return keyboard
