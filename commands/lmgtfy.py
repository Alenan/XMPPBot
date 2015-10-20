from re import match

from command import Command


class LMGTFY(Command):
    def match(self, room, nick, message):
        # let me google that for you
        m = match(r'''\.lmgtfy (["']?)(.*)\1''', message)
        if m:
            text = m.group(2)
            if not text:
                self.bot.msg_room(room, ' ')
            else:
                lmgtfy = "http://lmgtfy.com/?q="
                search = text.split(' ')
                for word in search:
                    lmgtfy = lmgtfy + "+" + word
                self.bot.msg_room(room, "I guess I can help you out: " + lmgtfy)
            return True

        return False
