from re import match

import commands
from command import Command
from extension import Extension


class ExecuteCommand(Extension):
    def __init__(self, *args, **kwargs):
        Extension.__init__(self, *args, **kwargs)

        # register all commands from the commands package
        self.commands = []
        for ActiveCommand in commands.__dict__.values():
            if isinstance(ActiveCommand, type) and \
               issubclass(ActiveCommand, Command):
                self.commands.append(ActiveCommand(self.bot))

        # use UniversalCommand as fallback
        self.commands.append(UniversalCommand(self.bot))

    def room_message(self, room, nick, message):
        for command in self.commands:
            if command.match(room, nick, message):
                break


class UniversalCommand(Command):
    def match(self, room, nick, message):
        m = match(r'\.([^ ]*) ?(.*)', message)
        if m:
            verb = m.group(1)
            rest = m.group(2)

            # third person singular form of verb (non-irregular)
            if verb.endswith('s') or verb.endswith('x'):
                verb += 'es'
            else:
                verb += 's'

            # genitive form of nick
            if not nick.endswith('s') and not nick.endswith('x'):
                nicks = nick + 's'
            else:
                nicks = nick

            # fix pronoums
            rest = rest.split(' ')
            for i, word in enumerate(rest):
                if word == 'me' or word == 'myself':
                    rest[i] = nick
                elif word == 'my':
                    rest[i] = nicks
                elif word == 'you':
                    rest[i] = 'they'
                elif word == 'your':
                    rest[i] = 'their'
                elif word == 'yourself':
                    rest[i] = 'themself'
            rest = ' '.join(rest)

            self.bot.msg_room(room, '/me %s %s' % (verb, rest))
            return True

        return False
