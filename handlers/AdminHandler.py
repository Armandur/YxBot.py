from MessageHandler import MessageHandler


class AdminHandler(MessageHandler):
    def handle_message(self, message):
        if message.find(":" + self.flags.getFlag("ADMIN") + "!") != -1:
                if message.find(self.bot._nick() + ": quit") != -1 and self.flags.getFlag("CAN_QUIT"):
                    print "-- Disconnecting --"
                    self.bot.disconnect()

                elif message.find(self.bot._nick() + ": reload") != -1:
                    self.bot._load()

                elif message.find(self.bot._nick() + ": count") != -1:
                    self.bot._sendMessage("Fabrikat: " + str(len(self.bot.yxfabrikat)) + ", Typer: " + str(len(self.bot.yxtyp)) + ", Kroppsdelar: " + str(len(self.bot.kroppsdel)))

                elif message.find(self.bot._nick() + ": list") != -1:
                    self.bot._sendMessage("Fabrikat: " + str(self.bot.yxfabrikat) + ", Typer: " + str(self.bot.yxtyp) + ", Kroppsdelar: " + str(self.bot.kroppsdel) + "\n")

                elif message.find(self.bot._nick() + ": raw") != -1 and self.flags.getFlag("RAW_ENABLED"):
                    text = message[message.find(": raw"):]
                    text = text.split(": raw")[1:]

                    self.bot.sock.send(text[0].strip() + "\n")
