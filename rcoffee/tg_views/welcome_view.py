from functools import partial
from telebot import types
from django.utils.translation import gettext as _

from rcoffee.tg_views.tg_view import TgView


class WelcomeView(TgView):
    langs = {
        'en': _('English'),
        'ru': _('Russian')
    }

    @staticmethod
    def commands():
        return {
            'start': WelcomeView.onMessage,
        }

    @staticmethod
    def callbacks():
        return {
            'language_code_en': partial(WelcomeView.switchLanguage, lang="en"),
            'language_code_ru': partial(WelcomeView.switchLanguage, lang="ru"),
        }

    def switchLanguage(self, message, lang):
        from rcoffee.tg_views.ask_password_view import AskPasswordView

        self.clear_keyboard(message, option=lang)
        self.bot.send_message(self.user_id, WelcomeView.langs[lang])

        self.change_view(AskPasswordView)

    def onMessage(self, _msg):
        answer = _('Hi! What language?')
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
            )
        )
        return keyboard
