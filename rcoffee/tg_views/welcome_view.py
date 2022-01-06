from telebot import types

from rcoffee.tg_views.tg_view import TgView
from rcoffee.orm import set_field, get_user, create_user
import rcoffee.views


class WelcomeView(TgView):

    @staticmethod
    def commands():
        return {
            'start': WelcomeView.onMessage,
            'help': WelcomeView.help,
        }

    @staticmethod
    def callbacks():
        return {
            'show_profile': WelcomeView.show,
            'change_profile': WelcomeView.changeProfile,
            'set_pause': WelcomeView.setPause,
            'set_run': WelcomeView.setRun,
            'back': WelcomeView.back
        }

    def back(self, message):
        self.args['base_message'] = message.id
        self.action()

    def show(self, message):
        user = get_user(self.user_id)
        answer = (
            'Вот так будет выглядеть твой профиль для собеседника:\n\n'
            f'{repr(user)}'
        )

        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(
            types.InlineKeyboardButton(
                text='Назад',
                callback_data='back'
            )
        )
        self.bot.send_chat_action(self.user_id, 'typing')
        self.bot.edit_message_text(answer, self.user_id, message_id=message.id, parse_mode='Markdown',
                                   reply_markup=keyboard)

    def setPause(self, message):
        set_field(self.user_id, 'is_active', False)
        self.bot.send_message(self.user_id, "Готово")

    def setRun(self, message):
        set_field(self.user_id, 'is_active', True)
        self.bot.send_message(self.user_id, "Готово")

    def action(self):
        user_id = self.user_id
        self.bot.send_chat_action(user_id, 'typing')
        text = 'Выбери подходящую опцию ниже'

        base_msg = self.args.pop('base_message', None)  # pop to sure edit message just once
        self.bot.set_state(self.user_id, repr(self))  # no more base_message so updating state
        if base_msg:
            self.bot.edit_message_text(text, user_id, base_msg,
                                       reply_markup=self.keyboard())
        else:
            self.bot.send_message(user_id, text,
                                  reply_markup=self.keyboard())

    def changeProfile(self, message):
        from rcoffee.tg_views.change_profile_view import ChangeProfileView
        self.change_view(ChangeProfileView(self.bot, self.user_id, {'base_message': message.id}))

    def help(self, _):
        self.action()

    def onMessage(self, message):
        from rcoffee.tg_views.enter_email_view import EnterEmailView

        user_id = self.user_id
        user = get_user(user_id)
        self.bot.send_chat_action(user_id, 'typing')

        if (not user or not user.is_verified) and message.from_user.username not in rcoffee.views.ADMINS:
            create_user(user_id)
            answer = ('Привет!🤩\n'
                      'Я Random Coffee бот 🤖\n\n'
                      'Каждую неделю я буду предлагать '
                      'тебе для встречи интересного человека, '
                      'случайно выбранного среди '
                      'других участников🎲\n\n')
            self.bot.send_message(user_id, answer)

            self.change_view(EnterEmailView(self.bot, user_id))
        elif not user and message.from_user.username in rcoffee.views.ADMINS:
            create_user(user_id)
            set_field(user_id, 'is_admin', True)
            set_field(user_id, 'is_verified', True)
            self.bot.send_message(user_id, ('Привет, админ!⭐\n\n'))
        else:
            answer = ('Рад тебя видеть!🔥\n'
                      'Если есть вопросы - /help')
            self.bot.send_message(user_id, answer)

    def keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 1

        keyboard.add(
            types.InlineKeyboardButton(
                text='Посмотреть свой профиль',
                callback_data='show_profile'
            ),
            types.InlineKeyboardButton(
                text='Поменять данные профиля',
                callback_data='change_profile'
            ),
            types.InlineKeyboardButton(
                text='Поставить на паузу',
                callback_data='set_pause'
            ),
            types.InlineKeyboardButton(
                text='Снять c паузы',
                callback_data='set_run'
            )
        )

        user = get_user(self.user_id)
        if user.is_admin:
            keyboard.add(
                types.InlineKeyboardButton(
                    text='Участники',
                    callback_data='show_users'
                ),
                types.InlineKeyboardButton(
                    text='Настройки пользователя',
                    callback_data='change_user'
                ),
                types.InlineKeyboardButton(
                    text='Пары',
                    callback_data='show_pairs'
                ),
                types.InlineKeyboardButton(
                    text='Сгенерировать пары',
                    callback_data='generate_pairs'
                ),
                types.InlineKeyboardButton(
                    text='Отправить приглашения',
                    callback_data='send_invites'
                )
            )
        return keyboard
