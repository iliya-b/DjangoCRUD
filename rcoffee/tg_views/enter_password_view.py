
from rcoffee.tg_views.tg_view import TgView
from django.utils.translation import gettext as _
from rcoffee.orm import (
    get_user,
    get_team_by_password
)


class EnterPasswordView(TgView):

    def onStart(self):
        answer = _('Enter password') + '\n'
        self.bot.send_message(self.user_id, answer)

    def onMessage(self, message):
        from rcoffee.tg_views.enter_field_view import EnterFieldView

        password = message.text
        user = get_user(self.user_id)
        team = get_team_by_password(password)

        if self.args.get('is_onboarding') and team:
            user.teams.add(team)
            answer = _('Correct') + '\n'
            self.bot.send_message(self.user_id, answer)

            self.change_view(EnterFieldView, {
                'field': 'name', 'is_onboarding': True})
        elif not self.args.get('is_onboarding') and team:
            user.teams.add(team)

            print('Team added')
        elif self.args.get('is_onboarding'):
            self.change_view(EnterPasswordView, {'is_onboarding': True})
        else:
            self.change_view(EnterPasswordView)
