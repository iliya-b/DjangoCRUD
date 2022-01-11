import importlib
import json

# Here we have mini-framework on top of telebot
from functools import lru_cache

from django.utils import translation

from rcoffee.utils import snake_casify


class TgView:

    @staticmethod
    def callbacks():
        return {}

    @staticmethod
    def commands():
        return {}

    def __init__(self, bot, user_id, args: dict = None):
        self.bot = bot
        self.user_id = user_id

        class StateDict(dict):

            def __setitem__(s, it, val):
                super().__setitem__(it, val)
                self.bot.set_state(self.user_id, repr(self))

            def __delitem__(s, it):
                super().__delitem__(it)
                self.bot.set_state(self.user_id, repr(self))

        self.args = StateDict(args or {})

    def __repr__(self):
        return json.dumps({
            'cls': self.__class__.__name__,
            'args': self.args
        })

    def onStart(self):
        pass

    def onMessage(self, message):
        pass

    def keyboard(self):
        pass

    def clear_keyboard(self, message, option=''):
        self.bot.edit_message_text(
            f'{message.text}\n\n🐱 {option}' if option else message.text,
            self.user_id,
            message.id
        )

    def change_view(self, _view, args=None):
        view = _view(self.bot, self.user_id, args)
        self.bot.set_state(self.user_id, repr(view))
        view.onStart()


def generate_tg_routes(bot, default_view):
    routes = []
    default_state = json.dumps({'cls': default_view.__name__, 'args': {}})

    @lru_cache(maxsize=None)
    def import_view(cls_name):
        module = importlib.import_module('rcoffee.tg_views.' + snake_casify(cls_name))
        return getattr(module, cls_name)

    def get_view_from_state(uid, state):
        state = json.loads(state)
        cls = import_view(state['cls'])
        return cls(bot, uid, state['args'])

    def get_view(uid):
        return get_view_from_state(uid, bot.get_state(uid) or default_state)

    def callback_handler(call):
        message = call.message
        translation.activate(call.from_user.language_code)
        name = call.data
        view = get_view(message.chat.id)
        bot.answer_callback_query(call.id)

        if name in view.callbacks():
            view.callbacks()[name](view, message)
        elif '*' in view.callbacks():
            view.callbacks()['*'](view, message, name)

    def command_handler(message):
        """
        Handler tries to execute command in this way:
        1. Looking for exact command in the view of the current state
        2. If there is not, looking for exact command in default view
        3. If there is not, check whether there is a broadcast (*) handler in the current view
        4. Then execute the first found command handler. If it is not found, do nothing
        :param message: message with a command from a user
        """
        translation.activate(message.from_user.language_code)
        name = message.text[1:]
        view = get_view(message.chat.id)

        if name in view.commands():
            view.commands()[name](view, message)
        elif name in default_view.commands():
            view = get_view_from_state(message.chat.id, default_state)
            view.commands()[name](view, message)
        elif '*' in view.commands():
            view.commands()['*'](view, message, name)

    def message_handler(message):
        translation.activate(message.from_user.language_code)

        get_view(message.chat.id) \
            .onMessage(message)

    # 1. listening for callbacks
    dec = bot.callback_query_handler(func=lambda call: True)
    routes.append(dec(callback_handler))

    # 2. listening for commands
    dec = bot.message_handler(regexp=r'^/(\w+)$')
    routes.append(dec(command_handler))

    # 3. listening for other messages
    dec = bot.message_handler(state='*')
    routes.append(dec(message_handler))
    return routes
