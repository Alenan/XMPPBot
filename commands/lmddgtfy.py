from re import match

from command import Command


class LMDDGTFY(Command):
    def match(self, room, nick, message):
        # let me ddg that for you
        m = match(r'''\.lmddgtfy (["']?)(.*)\1''', message)
        if m:
            text = m.group(2)
            if not text:
                self.bot.msg_room(room, ' ')
            else:
                lmddgtfy = "https://lmddgtfy.net/?q="
                search = text.split(' ')
                for word in search:
                    lmddgtfy = lmddgtfy + "%20" + word
                self.bot.msg_room(room, "I guess I can help you out like a duck could: " + lmddgtfy)
            return True

        return False
