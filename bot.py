import pytoml as toml
from xmpp import Client, JID, Message, NS_MUC, Presence

import extensions
from extension import Extension


class Bot(object):
    def __init__(self, config):
        self.config = config
        self.extensions = []
        self.rooms = []

    def run(self):
        user = self.config['user']['jid']
        password = self.config['user']['password']

        # connect to server
        self.client = client = Client(JID(user).getDomain(), debug=[])
        client.connect()
        if not client.auth(JID(user).getNode(), password,
                           resource=JID(user).getResource()):
            raise Exception('Unable to authorize.')

        # register handlers
        client.RegisterHandler('message', self.message_callback)
        client.RegisterHandler('presence', self.presence_callback)

        # send presence
        client.sendInitPresence()

        # join room(s)
        for room in self.config['room']:
            presence = Presence(to='%s/%s' % (room['jid'], room['nick']))
            presence.setTag('x', namespace=NS_MUC)\
                    .setTagData('password', room['password'])
            presence.getTag('x')\
                    .addChild('history', {'maxchars': '0', 'maxstanzas': '0'})
            client.send(presence)
            self.rooms.append(room['jid'])

        # process incoming messages
        while True:
            client.Process(1)

    def msg_room(self, room, message):
        self.send_msg(room, message, typ='groupchat')

    def send_msg(self, to, message, typ='chat'):
        self.client.send(Message(to=to, body=message, typ=typ))

    def register_extension(self, extension):
        self.extensions.append(extension)

    def message_callback(self, client, stanza):
        sender = stanza.getFrom()
        message = unicode(stanza.getBody())

        for room in self.rooms:
            if sender.bareMatch(room):
                nick = sender.getResource()
                for extension in self.extensions:
                    extension.room_message(room, nick, message)
                break
        else:
            for extension in self.extensions:
                extension.private_message(str(sender), message)

    def presence_callback(self, client, stanza):
        for extension in self.extensions:
            extension.presence(client, stanza)

if __name__ == '__main__':
    # read config in TOML format (https://github.com/toml-lang/toml#toml)
    with open('jupisnbg.cfg') as configfile:
        bot = Bot(toml.load(configfile))

    # register all extensions from the extensions package
    for ActiveExtension in extensions.__dict__.values():
        if isinstance(ActiveExtension, type) and \
           issubclass(ActiveExtension, Extension):
            bot.register_extension(ActiveExtension(bot))

    bot.run()   # never returns
