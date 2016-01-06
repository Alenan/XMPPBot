from random import choice, randint
from re import match

from command import Command


penis = ['penis', 'Penis.', 'Penis!', 'PENIS!!1einself']
vagina = ['vagina', 'Vagina.', 'Vagina!', 'VAGINA!!1einself']


class Penis(Command):
    def match(self, room, nick, message):
        # spam people
        m = match(r'\.penis ([^ ]+) ?(\d*)', message)
        if m:
            self.spam(room, nick, m.group(1), penis, m.group(2))
            return True

        m = match(r'\.vagina ([^ ]+) ?(\d*)', message)
        if m:
            self.spam(room, nick, m.group(1), vagina, m.group(2))
            return True

        return False

    def spam(self, room, aggressor, victim, messageset, num):
            if num:
                num = max(int(num), 1)
            else:
                num = randint(1, 100)

            if num > 100:
                victim = aggressor

            for i in xrange(num):
                self.bot.send_msg('%s/%s' % (room, victim), choice(messageset))
