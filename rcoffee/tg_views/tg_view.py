import json


class TgView:

    @staticmethod
    def callbacks():
        return {}

    @staticmethod
    def commands():
        return {}

    def __init__(self, bot, user_id, args=None):
        self.bot = bot
        self.user_id = user_id
        self.args = args or {}

    def __repr__(self):
        return json.dumps({
            'cls': self.__class__.__name__,
            'args': self.args
        })

    def action(self):
        pass

    def onData(self, message):
        pass

    def onMessage(self, message):
        pass

    def keyboard(self):
        pass

    def change_view(self, _view):
        self.bot.set_state(self.user_id, repr(_view))
        _view.action()


def generate_tg_routes(bot, default_view, callbacks=None, commands=None):
    routes = []
    from rcoffee.tg_views.change_profile_view import ChangeProfileView
    from rcoffee.tg_views.enter_email_view import EnterEmailView
    from rcoffee.tg_views.enter_password_view import EnterPasswordView
    from rcoffee.tg_views.enter_field_view import EnterFieldView
    from rcoffee.tg_views.welcome_view import WelcomeView

    _locals = locals()
    default_state = json.dumps({'cls': default_view.__name__, 'args': {}})

    # common handler for commands, callbacks and messages
    def handler(type):
        def _handler(call):
            if type == 'callback':
                message = call.message
                name = call.data
            elif type == 'command':
                message = call
                name = message.text[1:]
            else:
                name = message = call

            uid = message.chat.id
            state = bot.get_state(uid) or default_state
            print('request', state)

            state = json.loads(state)
            _view = _locals.get(state['cls'])(bot, uid, state['args'])

            if type == 'command' and name in _view.commands():
                _view.commands()[name](_view, message)
            if type == 'callback' and name in _view.callbacks():
                bot.answer_callback_query(call.id)
                _view.callbacks()[name](_view, message)
            if type == 'message':
                _view.onMessage(message)
        return _handler

    # 1. listening for callbacks
    dec = bot.callback_query_handler(func=lambda call: True)
    routes.append(dec(handler('callback')))

    # 2. listening for commands
    dec = bot.message_handler(regexp=r'^/(\w+)$')
    routes.append(dec(handler('command')))

    # 3. listening for other messages
    dec = bot.message_handler(state='*')
    routes.append(dec(handler('message')))
    return routes
