
from rcoffee.tg_views.tg_view import TgView
from django.utils.translation import gettext as _


class EnterPasswordView(TgView):

    def onStart(self):
        answer = _('Enter password') + '\n'
        self.bot.send_message(self.user_id, answer)

    def onMessage(self, message):
        from rcoffee.tg_views.enter_field_view import EnterFieldView

        answer = _('Correct') + '\n'
        self.bot.send_message(self.user_id, answer)

        self.change_view(EnterFieldView, {
            'field': 'name', 'is_onboarding': True})
