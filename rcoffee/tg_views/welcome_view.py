from functools import partial
from telebot import types
from django.utils.translation import gettext as _

from rcoffee.tg_views.tg_view import TgView


class WelcomeView(TgView):

    @staticmethod
    def commands():
        return {
            'start': WelcomeView.onMessage,
        }

    def onMessage(self, _msg):
        from rcoffee.tg_views.enter_password_view import EnterPasswordView

        answer = _('Welcome')
        self.bot.send_message(self.user_id, answer,
                              reply_markup=self.keyboard())

        self.change_view(EnterPasswordView, {'is_onboarding': True})
