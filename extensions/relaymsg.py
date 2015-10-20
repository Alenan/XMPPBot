from extension import Extension


class RelayMsg(Extension):
    def private_message(self, sender, message):
        sendertext = "[" + sender + "]: " + message
        for room in self.bot.rooms:
            self.bot.msg_room(room, sendertext)

    def room_message(self, room, nick, message):
        if "@jupisnbg" in message:
            # replied from group
            jupi_repliedby = nick
            jupi_message = message.replace("@jupisnbg", "")
            jupi_message = jupi_message.split(" ", 1)[1]
            receiver = jupi_message.split(" ", 1)[0]
            if "@" in receiver and "." in receiver:
                jupi_message = jupi_message.replace(receiver, "")
                jupi_reply = "[" + jupi_repliedby + "]: " + jupi_message
                self.bot.send_msg(receiver, jupi_reply)
            elif "--help" in receiver:
                self.bot.msg_room(room, "Usage: [at]jupisnbg full_jabber_id_of_recipient message.")
