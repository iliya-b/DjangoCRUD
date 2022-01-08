
from rcoffee.tg_views.tg_view import TgView
from django.utils.translation import gettext as _


class AskPasswordView(TgView):

    def onStart(self):
        answer = _('Enter password') + '\n'
        self.bot.send_message(self.user_id, answer)

    def onMessage(self, _msg):
        answer = _('Correct') + '\n'
        self.bot.send_message(self.user_id, answer)