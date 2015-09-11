"""
Usage: @jupisnbg <username_from_requestor> message

"""

from getpass import getpass
from xmpp import Client, NS_MUC, Presence
from xmpp.protocol import *

user = 'piggy'
server = 'jabber.ccc.de'
nick = 'bot'
password = getpass('Password for %s@%s:' % (user, server))
room = 'jupisnbg@conference.jabber.ccc.de'
room_password = getpass('Password for %s:' % (room))

def message_callback(client, stanza): # get msgs
    sender = stanza.getFrom()
    message = stanza.getBody()
    jid = '%s@%s' % (sender.getNode(), sender.getDomain())
    if jid == room:
	if "@jupisnbg" in message:
            #replied from group
            jupi_repliedby = sender.getResource()
            jupi_message = message.replace("@jupisnbg", "") 
            jupi_message = jupi_message.split(" ", 1)[1]
            receiver = jupi_message.split(" ", 1)[0]
            jupi_message = jupi_message.replace(receiver, "")
            jupi_reply = "[" + jupi_repliedby +  "]: " + jupi_message
            client.send(Message(to = receiver, body = jupi_reply, typ = "chat")) #wieso geht das nicht?
        print('%s: %s' % (sender.getResource(), message))
    else:
        sendertext = "[" + jid  + "]: " + message
        test = client.send(Message(to = room, body = sendertext, typ = "groupchat"))
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
