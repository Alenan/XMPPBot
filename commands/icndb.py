import json
from re import match
from urllib import urlopen

from command import Command


class ICNDB(Command):
    def match(self, room, nick, message):
        # query icndb
        m = match(r'\.icndb', message)
        if m:
            try:
                query = urlopen('http://api.icndb.com/jokes/random?escape=javascript&limitTo=explicit,nerdy')
                reply = json.loads(query.read())
                self.bot.msg_room(room, reply['value']['joke'].decode('string_escape'))
            except Exception:
                self.bot.msg_room(room, 'Chuck Norris can query ICNDB without getting an error.')
            return True

        return False
