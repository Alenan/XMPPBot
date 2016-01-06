from random import choice, randint
from re import match

from command import Command


class Penis(Command):
    def match(self, room, nick, message):
        # spam people
        m = match(r'\.(penis|vagina|anus) ([^ ]+) ?(\d*)', message)
        if m:
            word = m.group(1)
            messageset = [
                    word.lower(),
                    '%s.' % word.capitalize(),
                    '%s!' % word.capitalize(),
                    '%s!!einself' % word.upper()]
            self.spam(room, nick, m.group(2), messageset, m.group(3))
            return True

        return False

    def spam(self, room, aggressor, victim, messageset, num):
            if num:
                num = max(int(num), 1)
            else:
                num = randint(1, 100)

            if num > randint(1, 100):
                victim = aggressor

            for i in xrange(num):
                self.bot.send_msg('%s/%s' % (room, victim), choice(messageset))
