from MessageHandler import MessageHandler

class FlagEditHandler(MessageHandler):
    def handle_message(self, message):
         #EDITING FLAGS FROM CHAT
                if message.find(self.bot._nick() + ": setFlag") != -1 or message.find(self.bot._nick() + ": getFlag") != -1 or message.find(self.bot._nick() + ": delFlag") != -1:
                    print "-- EDITING FLAGS FROM CHAT --\n"

                    if message.find(self.bot._nick() + ": setFlag") != -1:
                        print "-- SET FLAG --\n"
                        splitted = message[message.find("setFlag"):].split()

                        if len(splitted) == 4: #1 setFlag, 2 flag, 3 type, 4 value ex, setFlag SILENT BOOL True => ['setFlag', 'SILENT', 'BOOL', 'True']
                            if splitted[2] == "STR":
                                self.flags.setFlag(splitted[1], splitted[3])
                            elif splitted[2] == "NUM":
                                value = -1
                                try:
                                    value = int(splitted[3])
                                except ValueError:
                                    value = -1

                                self.flags.setFlag(splitted[1], value)
                            elif splitted[2] == "BOOL":
                                value = False
                                if splitted[3] == "True":
                                    value = True
                                self.flags.setFlag(splitted[1], value)
                    elif message.find(self.bot._nick() + ": getFlag") != -1:
                        print "-- GET FLAG --\n"
                        splitted = message[message.find("getFlag"):].split()

                        if len(splitted) == 2: #1 getFlag, 2 flag
                            self.bot._sendMessage(splitted[1] + " : " + str(self.flags.getFlag(splitted[1])))

                        print self.flags._flags
                    elif message.find(self.bot._nick() + ": delFlag") != -1:
                        print "-- DEL FLAG --\n"
                        splitted = message[message.find("delFlag"):].split()

                        if len(splitted) == 2: #1 delFlag, 2 flag
                            self.flags.removeFlag(splitted[1])