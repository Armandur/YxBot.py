from Flags import Flags
from mock import *
import handlers
import unittest


class TestNicklistHandler(unittest.TestCase):
    def test_nicklist(self):
        flags = Flags()
        flags.setFlag("NICK", "BOT")
        flags.setFlag("CHANNEL", "#TEST")

        bot = DummyNicklistBot(flags)
        handler = handlers.NicklistHandler(bot, flags)

        message = ["irc.server.net 353 " + bot._nick() + " = #Test :@Op %HalfOp +Voice Normal\n", "irc.server.net 353 " + bot._nick() + " = #Test :Normal2 Normal3\n", "366 " + bot._nick()]

        for msg in message:
            handler.handle_message(msg)

        expectedNicks = set(["Op", "HalfOp", "Voice", "Normal", "Normal2", "Normal3"])
        self.assertItemsEqual(handler.bot.nicklist, expectedNicks)

if __name__ == '__main__':
    unittest.main()
