from rcoffee.orm import get_admins, get_user, set_field
from rcoffee.tg_views.tg_view import TgView
from rcoffee.views import SMTP


class EnterPasswordView(TgView):

    def onStart(self):
        if SMTP:
            answer = ('Отправил📮\n'
                      'Введи пароль из письма🔑')
        else:
            answer = ('Напиши админу, '
                      f'чтобы получить пароль ({", ".join(["@" + i for i in get_admins()])})🛡️\n'
                      'И введи его сюда🔑')

        self.bot.send_message(self.user_id, answer)

    def onMessage(self, message):
        from rcoffee.tg_views.enter_field_view import EnterFieldView

        user_id = message.from_user.id
        password = message.text
        user = get_user(user_id)

        if user.password == password:
            answer = 'Ты в системе🌐\n\n'
            self.bot.send_message(user_id, answer)

            set_field(user_id, 'is_verified', True)
            self.change_view(EnterFieldView, {'field': 'name', 'is_onboarding': True})
        else:
            answer = 'Попробуй еще раз\n'
            self.bot.send_message(user_id, answer)

    def keyboard(self):
        pass
