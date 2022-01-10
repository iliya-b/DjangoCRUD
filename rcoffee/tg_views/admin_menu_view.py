from typing import Optional

from telebot import types

from rcoffee.models import Team, User
from rcoffee.orm import set_field, get_user
from django.utils.translation import gettext as _
from rcoffee.tg_views.tg_view import TgView


class AdminMenuView(TgView):

    @staticmethod
    def callbacks():
        return {
            'back': AdminMenuView.back,
            'get_users': AdminMenuView.get_users,
            '*': AdminMenuView.select_team
        }

    def select_team(self, message, call_data):
        try:
            team_id = int(call_data[5:])
        except ValueError:
            return
        self.args['team_id'] = team_id

        self.bot.edit_message_text(_('Team selected'), self.user_id, self.args.get('base_message'),
                                   reply_markup=self.keyboard())

    def back(self, message):
        print('back')

    def get_users(self, message):
        from rcoffee.tg_views.admin_users_view import AdminUsersView
        self.change_view(AdminUsersView, self.args)

    def _teams(self):
        return Team.objects.filter(admin=get_user(self.user_id))

    def onStart(self):
        print(self._teams().count())
        if self._teams().count() == 1:
            print('1set')
            self.args['team_id'] = self._teams().first().id
            print('2set')

        self.bot.edit_message_text(_('Admin menu'), self.user_id, self.args.get('base_message'),
                                   reply_markup=self.keyboard())

    def keyboard(self):

        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 1

        if self._teams().count() > 1 and not self.args.get('team_id'):
            buttons = [
                types.InlineKeyboardButton(
                    text=team.name,
                    callback_data='team_%s' % team.id,
                ) for team in self._teams().all()]
            keyboard.add(*buttons)
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=_('Users'),
                    callback_data='get_users'
                ),
                types.InlineKeyboardButton(
                    text=_('User settings'),
                    callback_data='edit_user'
                ),
                types.InlineKeyboardButton(
                    text=_('Pairs'),
                    callback_data='get_pairs'
                ),
                types.InlineKeyboardButton(
                    text=_('Generate pairs'),
                    callback_data='generate_pairs'
                ),
                types.InlineKeyboardButton(
                    text=_('Send invites'),
                    callback_data='send_invites'
                ),
                types.InlineKeyboardButton(
                    text=_('Get password'),
                    callback_data='get_password'
                ),
                types.InlineKeyboardButton(
                    text=_('Generate password'),
                    callback_data='generate_password'
                ),
            )

        keyboard.add(
            types.InlineKeyboardButton(
                text=_('< Back'),
                callback_data='back'
            )
        )
        return keyboard
