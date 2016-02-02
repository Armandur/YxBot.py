from MessageHandler import MessageHandler

class KickedHandler(MessageHandler):
    def handle_message(self, message):
        if message.lower().find(str.lower("KICK " + self.flags.getFlag("CHANNEL") + " " + self.bot._nick())) != -1:
            print "-- Kicked from channel --\n"
            self.flags.setFlag("IN_CHANNEL", False)
