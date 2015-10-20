from re import match

from command import Command


class Say(Command):
    def match(self, room, nick, message):
        # say things
        m = match(r'''\.say (["']?)(.*)\1''', message)
        if m:
            text = m.group(2)
            if not text:
                self.bot.msg_room(room, ' ')
            else:
                self.bot.msg_room(room, text)
            return True

        return False
