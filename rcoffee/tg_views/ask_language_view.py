from telebot import types

from rcoffee.tg_views.tg_view import TgView
from rcoffee.orm import set_field, get_user, create_user
from tg_views.decorators import replace_keyboard_on_option


class AskLanguage(TgView):

    @staticmethod
    def callbacks():
        return {
            'language_code_en': AskLanguage.english,
            'language_code_ru': AskLanguage.russian,
        }

    @replace_keyboard_on_option('en')
    def english(self, _):
        self.bot.send_message(self.user_id, 'Английский')

    @replace_keyboard_on_option('ru')
    def russian(self, _):
        self.bot.send_message(self.user_id, 'Русский')

    def onMessage(self, _):
        answer = 'Какой язык?'
        self.bot.send_message(self.user_id, answer,
                              reply_markup=self.keyboard())

    def keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 2

        keyboard.add(
            types.InlineKeyboardButton(
                text='en',
                callback_data='language_code_en'
            ),
            types.InlineKeyboardButton(
                text='ru',
                callback_data='language_code_ru'
            ),
            types.InlineKeyboardButton(
                text='back',
                callback_data='back_'
            )
        )
        return keyboard
