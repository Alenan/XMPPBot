class Extension(object):
    def __init__(self, bot):
        self.bot = bot

    def private_message(self, sender, message):
        pass

    def room_message(self, room, nick, message):
        pass

    # XXX interface is xmpp specific
    # TODO define more abstract interface
    def presence(self, client, stanza):
        pass
