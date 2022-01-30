from datetime import datetime
from random import shuffle
from typing import Optional

from telebot import types

from rcoffee.models import Team, User, Pair
from rcoffee.orm import set_field, get_user
from django.utils.translation import gettext as _
from rcoffee.tg_views.tg_view import TgView


class AdminMenuView(TgView):

    @staticmethod
    def callbacks():
        return {
            'back': AdminMenuView.back,
            'get_users': AdminMenuView.get_users,
            'edit_user': AdminMenuView.edit_user,
            'get_pairs': AdminMenuView.get_pairs,
            '*': AdminMenuView.select_team
        }

    def generate_pairs(self):
        users = self._team().user_set.filter(is_active=True, is_blocked=False, is_verified=True).all()
        users = list(users)
        shuffle(users)

        if len(users) % 2 != 0:  # remove or append admin to get even count of participants
            admin = User.objects.get(pk=self.user_id)
            if admin in users:
                users.remove(admin)
            else:
                users.append(admin)

        pairs = [(users[i], users[i+1]) for i in range(0, len(users), 2)]
        print(pairs)


    def get_pairs(self, message):
        pairs = Pair.objects.filter(created_at__week=datetime.now().isocalendar()[1]).all()

        def _pair_line(pair):
            s = "%s & %s" % (pair.user_a.name if pair.user_a else "?", pair.user_b.name if pair.user_b else "?")
            if pair.feedback_a or pair.feedback_b:
                s += '(' + _('Got feedback') + ')'
            return s

        if pairs:
            self.bot.send_message(self.user_id, "\n".join(map(_pair_line, pairs)))
        else:
            self.bot.send_message(self.user_id, _('No pairs on this week'))

    def select_team(self, message, call_data):
        try:
            team_id = int(call_data[5:])
        except ValueError:
            return
        self.args['team_id'] = team_id

        self.bot.edit_message_text(_('Team selected'), self.user_id, self.args.get('base_message'),
                                   reply_markup=self.keyboard())

    def back(self, message):
        from rcoffee.tg_views.main_menu_view import MainMenuView
        self.change_view(MainMenuView, {'base_message': message.id,})

    def get_users(self, message):
        from rcoffee.tg_views.admin_users_view import AdminUsersView
        self.change_view(AdminUsersView, self.args)

    def edit_user(self, message):
        from rcoffee.tg_views.admin_user_info_view import AdminUserInfoView
        self.change_view(AdminUserInfoView, {'base_message': message.id, 'team_id': self.args['team_id']})

    def _teams(self):
        return Team.objects.filter(admin=get_user(self.user_id))

    def _team(self):
        return Team.objects.get(pk=self.args['team_id'])

    def onStart(self):
        if self._teams().count() == 1:
            self.args['team_id'] = self._teams().first().id

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
