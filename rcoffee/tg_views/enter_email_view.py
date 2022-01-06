from rcoffee.orm import set_field, get_admins, get_user
from rcoffee.tg_views.tg_view import TgView
from rcoffee.utils import is_correct_mail


class EnterEmailView(TgView):

    def onStart(self):
        self.bot.send_message(self.user_id,
                              ('Введи свой корпоративный mail, '
                               'чтобы получить пароль📧'))

    def onMessage(self, message):
        from rcoffee.tg_views.enter_password_view import EnterPasswordView

        user_id = message.from_user.id
        mail = message.text

        if is_correct_mail(mail):
            set_field(user_id, 'email', mail)
            admins = get_admins()
            user = get_user(user_id)

            print(user.password)

            for admin in admins:
                answer_to_admin = (
                    'Новый пользователь!\n'
                    f'@{message.from_user.username}\n'
                    f'[{message.from_user.first_name}](tg://user?id={user.telegram_id})\n'
                    f'{user.mail}\n'
                    f'{user.password}'
                )

                self.bot.send_message(admin.telegram_id,
                                      answer_to_admin, parse_mode='Markdown')

        if is_correct_mail(mail):
            self.change_view(EnterPasswordView(self.bot, user_id))
        else:
            self.onStart()

    def keyboard(self):
        pass
