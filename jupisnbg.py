from getpass import getpass
from re import match
from xmpp import Client, JID, Message, NS_MUC, Presence

user = 'moscito@jabber.ccc.de/vbot'
user_password = getpass('Password for %s:' % (user))
room = 'jupisnbg@conference.jabber.ccc.de'
room_password = getpass('Password for %s:' % (room))
nick = 'vbot'
extensions = {}

def message_callback(client, stanza):
    sender = stanza.getFrom()
    message = stanza.getBody()
    if sender.bareMatch(room):
        sender_nick = sender.getResource()
        print('[r] %s: %s' % (sender_nick, message))
        for extension in extensions.keys():
            if message.startswith('%s+%s' % (nick, extension)):
                send_msg(extensions[extension], ' '.join(message.split(' ')[1:]))
                return

        m = match('\.whois %s\+(.*)' % (nick), message)
        if m:
            extension = m.group(1)
            msg_room('%s+%s is %s.' % (nick, extension, extensions.get(extension, 'not managed')))
            return

        m = match('\.insult (.*)', message)
        if m:
            msg_room('%s is an idiot.' % (m.group(1)))
            return
    else:
        sender_nick = sender.getNode()
        print('[p] %s: %s' % (sender_nick, message))
        if not sender_nick in extensions.keys():
            # XXX nick collisions!
            join_room(sender_nick)
            extensions[sender_nick] = sender
        msg_room(message)

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

def msg_room(message):
    send_msg(room, message, typ='groupchat')

def send_msg(to, message, typ='chat'):
    client.send(Message(to=to, body=message, typ=typ))

# connect to server
client = Client(JID(user).getDomain(), debug=[])
client.connect()
while not client.auth(JID(user).getNode(), user_password, resource=JID(user).getResource()):
    print('Unable to authorize.')
    password = getpass('Password for %s:' % (user))

# register handlers
client.RegisterHandler('message', message_callback)
client.RegisterHandler('presence', presence_callback)

# send presence
client.sendInitPresence()
join_room()

# process incoming messages
while True:
    client.Process(1)
