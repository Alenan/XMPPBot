from getpass import getpass
from re import match
from xmpp import Client, JID, Message, NS_MUC, Presence

user = 'moscito@jabber.ccc.de'
user_password = getpass('Password for %s:' % (user))
room = 'jupisnbg@conference.jabber.ccc.de'
room_password = getpass('Password for %s:' % (room))
nick = 'bot'
extensions = {}

def message_callback(client, stanza):
    sender = stanza.getFrom()
    message = stanza.getBody()
    if sender.bareMatch(room):
        nick = sender.getResource()
        print('[r] %s: %s' % (nick, message))
        for extension in extensions.keys():
            if message.startswith('%s+%s' % (nick, extension)):
                send_msg(extensions[extension], ' '.join(message.split(' ')[1:]))

        m = match('\.whois %s\+(.*)' % (nick), message)
        if m:
            extension = m.group(1)
            msg_room(body='%s+%s is %s.' % (nick, extension, extensions.get(extension, 'not managed')))

        m = match('\.insult (.*)', message)
        if m:
            msg_room(body='%s is an idiot.' % (m.group(1)))
    else:
        nick = sender.getNode()
        print('[p] %s: %s' % (nick, message))
        if not nick in extensions.keys():
            # XXX nick collisions!
            join_room(nick)
            extensions[nick] = sender
        msg_room(nick, message)

def presence_callback(client, stanza):
    # not used yet
    pass

def join_room(extension=None):
    if extension:
        presence = Presence(to='%s/%s+%s' % (room, nick, extension))
    else:
        presence = Presence(to='%s/%s' % (room, nick))
    presence.setTag('x', namespace=NS_MUC).setTagData('password', room_password)
    client.send(presence)

def msg_room(extension=None, body=None):
    if extension:
        send_msg('%s/%s+%s' % (room, nick, extension), body)
    else:
        send_msg('%s/%s' % (room, nick), body)

def send_msg(to, body):
    message = Message(to=to, body=body)
    client.send(message)

# connect to server
client = Client(JID(user).getDomain(), debug=[])
client.connect()
while not client.auth(JID(user).getNode(), user_password):
    print('Unable to authorize.')
    password = getpass('Password for %s:' % (user))

# register handlers
client.RegisterHandler('message', message_callback)
client.RegisterHandler('presence', presence_callback)

# send presence
#client.sendInitPresence()
join_room()

# process incoming messages
while True:
    client.Process(1)
