def replace_keyboard_on_option(option):
    def wrapper(function):
        def wrapper_(self, message):
            self.bot.edit_message_text(
                f'{message.text}\n\n🐱 {option}',
                self.user_id,
                message.id
            )
            function(self, message)
        return wrapper_
    return wrapper
