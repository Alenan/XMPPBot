from re import match
from urllib import urlopen

from command import Command


class Kitten(Command):
    def match(self, room, nick, message):
        m = match(r'\.kitten', message)
        if m:
            link = urlopen('http://random.cat/meow')
            pic = link.read()
            self.bot.msg_room(room, "uhm... ok. Here is a picture of a cute cat: %s." % (pic))
            return True

        return False
