import random
from yxbot import YxBot
from Flags import Flags

random.seed()
flags = Flags()

# flags.setFlag("CONNECTION", ("portlane.se.quakenet.org", 6667))
# flags.setFlag("CHANNEL", "#anrop.net")
# flags.setFlag("NICK", "Yxbotten")
# flags.setFlag("PATHS", ["yxfabrikat.txt", "yxtyp.txt", "kroppsdel.txt"])
# flags.setFlag("ADMIN", "Armandur")
# flags.setFlag("SILENT", False)
# flags.setFlag("USERS_ONLY", False)

# flags.setFlag("CONNECTION", ("irc.snoonet.org", 6667))
# flags.setFlag("CHANNEL", "#sweden")
# flags.setFlag("NICK", "YxBot")
# flags.setFlag("PATHS", ["yxfabrikat.txt", "yxtyp.txt", "kroppsdel.txt"])
# flags.setFlag("ADMIN", "Armandur")
# flags.setFlag("SILENT", False)
# flags.setFlag("USERS_ONLY", False)

flags.setFlag("CONNECTION", ("irc.oftc.net", 6667))
flags.setFlag("CHANNEL", "#armandur_test")
flags.setFlag("NICK", "YxBot")
flags.setFlag("PATHS", ["yxfabrikat.txt", "yxtyp.txt", "kroppsdel.txt"])
flags.setFlag("ADMIN", "Armandur")
flags.setFlag("SILENT", False)
flags.setFlag("USERS_ONLY", False)

bot = YxBot(flags)
bot.connect()
