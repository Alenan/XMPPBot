from getpass import getpass
from xmpp import Client, NS_MUC, Presence

user = 'moscito'
server = 'jabber.ccc.de'
nick = 'bot'
password = getpass('Password for %s@%s:' % (user, server))
room = 'jupisnbg@conference.jabber.ccc.de'
room_password = getpass('Password for %s:' % (room))

def message_callback(client, stanza):
    sender = stanza.getFrom()
    message = stanza.getBody()
    jid = '%s@%s' % (sender.getNode(), sender.getDomain())
    if jid == room:
        print('%s: %s' % (sender.getResource(), message))
    else:
        print('%s: %s' % (sender.getNode(), message))

client = Client(server, debug=[])
client.connect()
while not client.auth(user, password):
    print('Unable to authorize.')
    password = getpass('Password for %s@%s:' % (user, server))
client.RegisterHandler('message', message_callback)
client.sendInitPresence()
presence = Presence(to='%s/%s' % (room, nick))
presence.setTag('x', namespace=NS_MUC).setTagData('password', room_password)
client.send(presence)
while True:
    client.Process(1)
