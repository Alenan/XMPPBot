from getpass import getpass
from xmpp import Client

user = 'moscito90'
server = 'jabber.ccc.de'
password = getpass('Password for %s@%s:' % (user, server))

def message():
    pass

client = Client(server)
client.connect()
while not client.auth(user, password):
    print('Unable to authorize.')
    password = getpass('Password for %s@%s:' % (user, server))
client.RegisterHandler('message', message)
client.sendInitPresence()
client.Process(1)
