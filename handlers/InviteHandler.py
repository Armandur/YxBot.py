from MessageHandler import MessageHandler


class InviteHandler(MessageHandler):
    def handle_message(self, message):
        if message.find("INVITE " + self.bot._nick()) != -1 and not self.flags.getFlag("IN_CHANNEL"):
            splitted = message[message.find("INVITE " + self.bot._nick() + " :"):].split()

            if len(splitted) == 3:
                chan = splitted[2][1:]
                print "-- Received INVITE to " + chan + " --\n"
                return True

        return False
