from re import match

from command import Command


class Insult(Command):
    def match(self, room, nick, message):
        # insult people
        m = match(r'\.insult (.*)', message)
        if m:
            self.bot.msg_room(room, '%s is an idiot.' % (m.group(1)))
            return True

        return False
