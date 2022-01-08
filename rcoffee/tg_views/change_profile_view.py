from functools import partial
from django.utils.translation import gettext as _

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
        from rcoffee.tg_views.welcome_view import WelcomeView
        self.change_view(WelcomeView, {'base_message': message.id})

    def moveToField(self, message, field):
        from rcoffee.tg_views.enter_field_view import EnterFieldView
        self.change_view(EnterFieldView, {'field': field})

    def onStart(self):
        self.bot.edit_message_text(_('Change profile data'), self.user_id, self.args['base_message'],
                                   reply_markup=self.keyboard())

    def onMessage(self, _msg):
        self.bot.send_message(self.user_id, _('?'))

    def keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 1

        keyboard.add(
            types.InlineKeyboardButton(
                text=_('My name'),
                callback_data='change_name'
            ),
            types.InlineKeyboardButton(
                text=_('My social link'),
                callback_data='change_link'
            ),
            types.InlineKeyboardButton(
                text=_('Where do I work'),
                callback_data='change_work'
            ),
            types.InlineKeyboardButton(
                text=_('About me'),
                callback_data='change_about'
            ),
            types.InlineKeyboardButton(
                text=_('Back'),
                callback_data='back'
            )
        )
        return keyboard
