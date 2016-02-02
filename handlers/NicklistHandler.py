from MessageHandler import MessageHandler

class NicklistHandler(MessageHandler):

    nicklistBuffer = ""

    def handle_message(self, message):
        if message.find("PART") != -1 or message.find("JOIN") != -1 or message.find("NICK") != -1 or message.find("QUIT") != -1:
            self.bot._getNicks()
        elif message.lower().find(str("353 " + self.bot._nick() + " = " + self.flags.getFlag("CHANNEL") + " :").lower()) != -1:
            self.nicklistBuffer += message
        elif message.find("366 " + self._nick()) != -1:
            self._updateNicklist(self.nicklistBuffer)
            self.nicklistBuffer = ""

    def _updateNicklist(self, message):
        print "-- Updating NickList --\n"
        self.bot.nicklist = set()

        message = message.splitlines()

        nicks = set()
        for s in message:
            t = s[s.find("#"):].split()
            t = t[1:]
            nicks.add(t)

        nicks = [s.strip('@') for s in nicks]
        nicks = [s.strip('%') for s in nicks]
        nicks = [s.strip('+') for s in nicks]
        nicks = [s.strip(':') for s in nicks]
        self.bot.nicklist = nicks


        print "NickList contains: "
        print sorted(self.bot.nicklist)