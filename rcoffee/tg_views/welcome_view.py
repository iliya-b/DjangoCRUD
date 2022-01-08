from functools import partial
from telebot import types
from django.utils.translation import gettext as _

from rcoffee.tg_views.tg_view import TgView
from rcoffee.orm import (
    create_user
)


class WelcomeView(TgView):

    @staticmethod
    def commands():
        return {
            'start': WelcomeView.onMessage,
            'help': WelcomeView.onMessage
        }

    def onStart(self):
        self.bot.send_message(self.user_id, _('Welcome'))

    def onMessage(self, message):
        from rcoffee.tg_views.enter_password_view import EnterPasswordView
        from rcoffee.tg_views.main_menu_view import MainMenuView

        answer = _('Welcome')

        user = create_user(self.user_id)

        if not user.teams.exists():
            self.bot.send_message(self.user_id, answer,
                                  reply_markup=self.keyboard())

            self.change_view(EnterPasswordView, {'is_onboarding': True})
        else:
            self.change_view(MainMenuView)
