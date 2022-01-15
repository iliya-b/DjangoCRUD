from typing import Optional

from telebot import types

from rcoffee.models import Team, User
from rcoffee.orm import set_field, get_user
from django.utils.translation import gettext as _
from rcoffee.tg_views.tg_view import TgView


class MainMenuView(TgView):

    @staticmethod
    def callbacks():
        return {
            'show_profile': MainMenuView.show_profile,
            'change_profile': MainMenuView.change_profile,
            'show_teams': MainMenuView.show_teams,
            'show_status': MainMenuView.show_status,
            'show_admin': MainMenuView.show_admin,
            'back': MainMenuView.back
        }

    def show_admin(self, message):
        from rcoffee.tg_views.admin_menu_view import AdminMenuView
        self.change_view(AdminMenuView, {'base_message': message.id})

    def show_profile(self, message):
        from rcoffee.tg_views.show_profile_view import ShowProfileView
        self.change_view(ShowProfileView, {'base_message': message.id})

    def change_profile(self, message):
        from rcoffee.tg_views.change_profile_view import ChangeProfileView
        self.change_view(ChangeProfileView, {'base_message': message.id})

    def show_teams(self, message):
        from rcoffee.tg_views.change_teams_view import ChangeTeamsView
        self.change_view(ChangeTeamsView, {'base_message': message.id})

    def show_status(self, message):
        from rcoffee.tg_views.show_status_view import ShowStatusView
        self.change_view(ShowStatusView, {'base_message': message.id})

    def back(self, message):
        print('back')

    def onStart(self):
        if 'base_message' in self.args:
            self.bot.edit_message_text(_('Main menu'),
                                       self.user_id,
                                       self.args['base_message'],
                                       reply_markup=self.keyboard())
        else:
            self.bot.send_message(
                self.user_id, _('Main menu'), reply_markup=self.keyboard())


    def keyboard(self):
        is_admin = Team.objects.filter(admin=get_user(self.user_id)).exists()

        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 1

        if is_admin:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=_('Admin'),
                    callback_data='show_admin'
                ),
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=_('Show profile'),
                callback_data='show_profile'
            ),
            types.InlineKeyboardButton(
                text=_('Change profile'),
                callback_data='change_profile'
            ),
            types.InlineKeyboardButton(
                text=_('My teams'),
                callback_data='change_teams'
            ),
            types.InlineKeyboardButton(
                text=_('Status'),
                callback_data='show_status'
            ),
            types.InlineKeyboardButton(
                text=_('Back'),
                callback_data='back'
            )
        )
        return keyboard
