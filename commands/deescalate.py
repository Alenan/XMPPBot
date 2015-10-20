from random import choice
from re import match

from command import Command


class Deescalate(Command):
    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)

        # read mlp files
        with open('mlp/s5e14') as f:
            self.mlp = f.read().splitlines()

    def match(self, room, nick, message):
        # CAPS LOCK MLP TRIGGER
        wordlist = message.split()
        capslock = 0
        for word in wordlist:
            if (word.isupper() == True) and (len(word) > 2):    # more than 2 letters and capslocked
                capslock = capslock + 1
        if capslock > 2:    # more than 3 caps locked words
            self.bot.msg_room(room, "Okay, calm down " + nick + " and watch this: " + choice(self.mlp))
            return True

        # random mlp episode
        m = match(r'\.deescalate', message)
        if m:
            self.bot.msg_room(room, "Okay, everybody calm down and watch this: " + choice(self.mlp))
            return True

        return False
