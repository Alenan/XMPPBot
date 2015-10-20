from random import randint
from re import match

from command import Command


class Dice(Command):
    def match(self, room, nick, message):
        # throw a dice
        m = match(r'\.dice (\d+)', message)
        if m:
            faces = int(m.group(1))
            self.bot.msg_room(room, '/me rolls a dice with %d faces.' % (faces))
            if faces:
                self.bot.msg_room(room, 'The dice shows %d (trust me).' % (randint(1, faces)))
            else:
                self.bot.msg_room(room, 'fuck you. -.-')
            return True

        return False
