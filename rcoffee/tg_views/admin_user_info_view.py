from django.db.models import F, Func, Model
from telebot import types
from telebot.apihelper import ApiTelegramException

from rcoffee.models import User
from rcoffee.orm import set_field, get_user
from django.utils.translation import gettext as _
from rcoffee.tg_views.tg_view import TgView
from rcoffee.utils import Not


class AdminUserInfoView(TgView):

    @staticmethod
    def callbacks():
        return {
            'back': AdminUserInfoView.back,
            'toggle_block': AdminUserInfoView.toggle_block,
            'toggle_active': AdminUserInfoView.toggle_active,
        }

    def toggle_block(self, message):
        user = self._user()
        user.is_blocked = not user.is_blocked
        user.save()
        self._user_info(user, base_message=message.id)

    def toggle_active(self, message):
        user = self._user()
        user.is_active = not user.is_active
        user.save()
        self._user_info(user, base_message=message.id)

    def back(self, message):
        from rcoffee.tg_views.admin_menu_view import AdminMenuView
        self.change_view(AdminMenuView, {'base_message': message.id})

    def _user_info(self, user, base_message=None):
        text = _('Profile') + str(user)
        if base_message:
            self.bot.edit_message_text(
                text, self.user_id, base_message,
                reply_markup=self.keyboard()
            )
        else:
            self.bot.send_message(
                self.user_id, text,
                reply_markup=self.keyboard()
            )

    def _user(self):
        return User.objects.get(pk=self.args['user_id'])

    def onStart(self):
        if 'user_id' in self.args:
            self._user_info(self._user())
        else:
            self.bot.send_message(
                self.user_id,
                _('Enter user id:'),
            )

    def onMessage(self, message):
        try:
            id = int(message.text)
            user = User.objects.get(telegram_id=id, teams__id__in=[self.args['team_id']])
            self.args['user_id'] = user.id
        except (ValueError, User.DoesNotExist):
            self.bot.send_message(
                self.user_id,
                _('User not found!'),
            )

        self.onStart()

    def keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 2

        user = self._user()

        btn_block = \
            types.InlineKeyboardButton(
                text=_('Unblock user' if user.is_blocked else 'Block user'),
                callback_data='toggle_block'
            )

        btn_activate = \
            types.InlineKeyboardButton(
                text=_('Pause user' if user.is_active else 'Activate user'),
                callback_data='toggle_active'
            )

        keyboard.add(btn_block, btn_activate)

        keyboard.add(
            types.InlineKeyboardButton(
                text=_('< Back'),
                callback_data='back'
            )
        )
        return keyboard
