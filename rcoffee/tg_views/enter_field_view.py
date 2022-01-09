from typing import Optional

from telebot import types

from rcoffee.orm import (
    get_user,
    set_field
)
from django.utils.translation import gettext as _
from rcoffee.tg_views.tg_view import TgView


class EnterFieldView(TgView):
    messages = {
        'name': _('My name'),
        'about': _('About me'),
        'work': _('Where do I work'),
        'link': _('My social link')
    }

    def onStart(self):
        self.bot.send_message(
            self.user_id, EnterFieldView.messages[self.args['field']])

    def onMessage(self, message):
        from rcoffee.tg_views.welcome_view import WelcomeView

        field_value = message.text
        user = get_user(self.user_id)

        if self.args.get('is_onboarding') and self.args['field'] == 'name':
            set_field(user, 'name', field_value)
            self.bot.send_message(self.user_id, _('Glad to meet you!'))
            self.change_view(EnterFieldView, {
                             'field': 'link', 'is_onboarding': True})
        elif self.args.get('is_onboarding') and self.args['field'] == 'link':
            set_field(user, 'link', field_value)
            self.bot.send_message(self.user_id, _('Done'))

            self.change_view(WelcomeView)
