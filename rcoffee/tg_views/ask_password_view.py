
from rcoffee.tg_views.tg_view import TgView


class AskPasswordView(TgView):

    def onStart(self):
        answer = 'Введи пароль\n'
        self.bot.send_message(self.user_id, answer)

    def onMessage(self, _):
        answer = 'Правильно\n'
        self.bot.send_message(self.user_id, answer)