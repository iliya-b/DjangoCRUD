from functools import partial

from telebot import types

import rcoffee.tg_views.enter_field_view
from rcoffee.tg_views.tg_view import TgView


class ChangeProfileView(TgView):

    @staticmethod
    def callbacks():
        return {
            'change_link': partial(ChangeProfileView.moveToField, field='link'),
            'change_name': partial(ChangeProfileView.moveToField, field='name'),
            'change_about': partial(ChangeProfileView.moveToField, field='about'),
            'change_work': partial(ChangeProfileView.moveToField, field='work'),
            'back': ChangeProfileView.back
        }

    def back(self, message):
        self.change_view(rcoffee.tg_views.welcome_view.WelcomeView(self.bot, self.user_id, {'base_message': message.id}))

    def moveToField(self, message, field):
        self.change_view(rcoffee.tg_views.enter_field_view.EnterFieldView(self.bot, self.user_id, {'field': field}))

    def action(self):
        self.bot.edit_message_text('👉 Поменять данные профиля', self.user_id, self.args['base_message'],
                                   reply_markup=self.keyboard())

    def onMessage(self, _):
        self.bot.send_message(self.user_id, 'не понял')

    def keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 1

        keyboard.add(
            types.InlineKeyboardButton(
                text='Своё имя',
                callback_data='change_name'
            ),
            types.InlineKeyboardButton(
                text='Ссылку на социальную сеть',
                callback_data='change_link'
            ),
            types.InlineKeyboardButton(
                text='Кем работаю',
                callback_data='change_work'
            ),
            types.InlineKeyboardButton(
                text='О себе',
                callback_data='change_about'
            ),
            types.InlineKeyboardButton(
                text='Назад',
                callback_data='back'
            )
        )
        return keyboard
