from extension import Extension


class PrintMsg(Extension):
    def private_message(self, sender, message):
        print(('[%s]: %s' % (sender, message)).encode('utf-8'))

    def room_message(self, room, nick, message):
        print(('[%s] %s: %s' % (room, nick, message)).encode('utf-8'))
