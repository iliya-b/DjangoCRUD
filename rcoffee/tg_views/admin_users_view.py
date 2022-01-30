import math
from telebot import types
from rcoffee.models import Team, User
from django.utils.translation import gettext as _
from rcoffee.tg_views.tg_view import TgView


class AdminUsersView(TgView):
    page_size = 5

    @staticmethod
    def callbacks():
        return {
            'back': AdminUsersView.back,
            '*': AdminUsersView.select_page
        }

    @staticmethod
    def commands():
        return {
            '*': AdminUsersView.info
        }

    def info(self, message, cmd):
        user_id = int(cmd[4:])
        from rcoffee.tg_views.admin_user_info_view import AdminUserInfoView
        self.change_view(AdminUserInfoView, {'user_id': user_id, 'team_id': self.args['team_id']})

    def _users(self):
        return User.objects.filter(teams__in=[self.args['team_id']])

    def _team(self):
        return Team.objects.get(pk=self.args['team_id'])

    def select_page(self, message, page):
        page = int(page[5:])
        self.args['current_page'] = page
        self.render_page()

    def back(self, message):
        from rcoffee.tg_views.admin_menu_view import AdminMenuView
        self.change_view(AdminMenuView, self.args)

    def _page_code(self, num):
        return 'page_%d' % num

    def onStart(self):
        self.args['current_page'] = self.args.get('current_page', 1)
        self.render_page()

    def render_page(self):
        users = self._team().user_set.all()
        msg = "\n\n".join(map(self._user_line, users))
        self.bot.edit_message_text(_('Users list') + "\n\n" + msg, self.user_id, self.args['base_message'],
                                   reply_markup=self.keyboard())

    def _user_line(self, user: User):
        return str(user) + " / " + _("Info") + (": /info%d" % user.id)

    def keyboard(self):
        count = self._users().count()
        page_count = math.ceil(count / self.page_size)
        current_page = self.args['current_page']

        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 3

        row = []
        if current_page > 1:
            row.append(
                types.InlineKeyboardButton(text='←', callback_data=self._page_code(max(1, current_page - 1))),
            )
        if page_count > 1:
            row.append(
                types.InlineKeyboardButton(
                    text=str(current_page),
                    callback_data=self._page_code(current_page)
                ),
            )
        if current_page < page_count:
            types.InlineKeyboardButton(text='→', callback_data=self._page_code(min(page_count, current_page + 1)))

        keyboard.add(*row)
        keyboard.add(
            types.InlineKeyboardButton(text=_('< Back'), callback_data='back')
        )

        return keyboard
