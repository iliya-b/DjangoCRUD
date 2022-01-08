from typing import Optional

from telebot import types

from rcoffee.orm import set_field
from django.utils.translation import gettext as _
from rcoffee.tg_views.tg_view import TgView


class EnterFieldView(TgView):
    messages = {
        'name': _('My name'),
        'about': _('About me'),
        'work': _('Where do I work'),
        'link': _('My social link')
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
        self.bot.send_message(
            self.user_id, EnterFieldView.messages[self.args['field']])

    def onMessage(self, message):
        from rcoffee.tg_views.welcome_view import WelcomeView
        set_field(self.user_id, self.args['field'], message.text)

        if not self.args.get('is_onboarding', False):
            self.bot.send_message(self.user_id, _('Done'),
                                  reply_markup=self.keyboard())
        elif self.args['field'] == 'name':
            self.bot.send_message(self.user_id, _('Glad to meet you!'))
            self.change_view(EnterFieldView, {
                             'field': 'link', 'is_onboarding': True})
        else:
            msg = _('Alright! All done')
            self.bot.send_message(self.user_id, msg)
            self.change_view(WelcomeView)

    def keyboard(self) -> Optional[types.InlineKeyboardMarkup]:
        if not self.args.get('is_onboarding', False):
            keyboard = types.InlineKeyboardMarkup()

            keyboard.add(
                types.InlineKeyboardButton(
                    text=_('Back'),
                    callback_data='back'
                )
            )
            return keyboard
        return None
