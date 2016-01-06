from random import choice, randint
from re import match

from command import Command


penis = ['penis', 'Penis.', 'Penis!', 'PENIS!!1einself']


class Penis(Command):
    def match(self, room, nick, message):
        # spam people
        m = match(r'\.penis ([^ ]+) ?(\d*)', message)
        if m:
            num = m.group(2)
            if num:
                num = min(max(int(num), 0), 100)
            else:
                num = randint(1, 100)
            for i in xrange(num):
                self.bot.send_msg('%s/%s' % (room, m.group(1)), choice(penis))
            return True

        return False
