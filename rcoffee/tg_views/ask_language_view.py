from functools import partialmethod, partial

from telebot import types

from rcoffee.tg_views.tg_view import TgView
from rcoffee.orm import set_field, get_user, create_user


class AskLanguage(TgView):
    langs = {
        'en': 'Английский',
        'ru': 'Русский'
    }

    @staticmethod
    def callbacks():
        return {
            'language_code_en': partial(AskLanguage.switchLanguage, lang="en"),
            'language_code_ru': partial(AskLanguage.switchLanguage, lang="ru"),
        }

    def switchLanguage(self, message, lang):
        self.clear_keyboard(message, option=lang)
        self.bot.send_message(self.user_id, AskLanguage.langs[lang])

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
