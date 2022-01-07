from typing import Optional

from telebot import types

from rcoffee.orm import set_field
import rcoffee.tg_views.change_profile_view
from rcoffee.tg_views.tg_view import TgView


class EnterFieldView(TgView):
    messages = {
        'name': 'Как тебя зовут?',
        'about': 'Напиши о себе',
        'work': 'Чем ты занимаешься?',
        'link': 'Пришли ссылку на свой профиль '
                'в любой социальной сети. '
                'Так вы в паре сможете лучше узнать '
                'друг о друге до встречи🔎'
    }

    @staticmethod
    def callbacks():
        return {
            'back': EnterFieldView.back
        }

    def back(self, message):
        from rcoffee.tg_views.change_profile_view import ChangeProfileView
        self.change_view(ChangeProfileView, {'base_message': message.id})

    def onStart(self):
        self.bot.send_message(self.user_id, EnterFieldView.messages[self.args['field']])

    def onMessage(self, message):
        from rcoffee.tg_views.welcome_view import WelcomeView
        set_field(self.user_id, self.args['field'], message.text)

        if not self.args.get('is_onboarding', False):
            self.bot.send_message(self.user_id, 'Готово', reply_markup=self.keyboard())
        elif self.args['field'] == 'name':
            self.bot.send_message(self.user_id, 'Рад познакомиться!)')
            self.change_view(EnterFieldView, {'field': 'link', 'is_onboarding': True})
        else:
            msg = ('Отлично, все готово!✨\n\n'
                   'Свою пару для встречи ты будешь узнавать'
                   ' каждый понедельник — сообщение придет в этот чат\n\n'
                   'Напиши партнеру в Telegram, '
                   'чтобы договориться о встрече или звонке\n'
                   'Время и место вы выбираете сами\n\n'
                   'Если остались вопросы - /help!)')
            self.bot.send_message(self.user_id, msg)
            self.change_view(WelcomeView)

    def keyboard(self) -> Optional[types.InlineKeyboardMarkup]:
        if not self.args.get('is_onboarding', False):
            keyboard = types.InlineKeyboardMarkup()

            keyboard.add(
                types.InlineKeyboardButton(
                    text='Назад',
                    callback_data='back'
                )
            )
            return keyboard
        return None
