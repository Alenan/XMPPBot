from glob import glob
from os.path import basename
from random import choice
from re import match

from command import Command


class Joke(Command):
    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)

        # read joke files
        self.jokes = {}
        for filename in glob('witze/*'):
            with open(filename) as f:
                self.jokes[basename(filename)] = f.read().splitlines()
        self.jokes[''] = sum(self.jokes.values(), [])

    def match(self, room, nick, message):
        # make a joke
        m = match(r'\.joke ?(.*)', message)
        if m:
            category = m.group(1)
            try:
                self.bot.msg_room(room, choice(self.jokes[category]))
            except KeyError:
                self.bot.msg_room(room, choice(self.jokes['']))
            return True

        return False
