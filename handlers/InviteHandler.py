from MessageHandler import MessageHandler

class InviteHandler(MessageHandler):

        def handle_message(self, message):
            # :Armandur!~Rasmus@c-c6c1e055.03-48-68736410.cust.bredbandsbolaget.se INVITE YxBot :#armandur_test
            if message.find("INVITE " + self.bot._nick()) != -1 and not self.flags.getFlag("IN_CHANNEL"):
                splitted = message[message.find("INVITE " + self.bot._nick() + " :"):].split()

                if len(splitted) == 3:
                    chan = splitted[2][1:]
                    print "-- Received INVITE to " + chan + " --\n"
                    return True

            return False