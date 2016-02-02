from MessageHandler import MessageHandler

class PingHandler(MessageHandler):
    def pong(self, ping):
        print "-- Answering PING with PONG :" + ping + " --\n"
        self.bot.send("PONG :" + ping + "\n")

    def handle_message(self, message):
        if message.find("PING :") != -1:
            ping = message.split()[1][1:]
            self.pong(ping)
