from Flags import Flags
from mock import *
import handlers
import unittest

class TestInviteHandler(unittest.TestCase):

    def test_invited(self):
        flags = Flags()
        flags.setFlag('CHANNEL', 'TEST')
        flags.setFlag('IN_CHANNEL', False)
        flags.setFlag('NICK', 'BOT')

        bot = DummyBot(flags)
        handler = handlers.InviteHandler(bot, flags)
        self.assertTrue(handler.handle_message("INVITE BOT :#NEW_TEST"))
        self.assertTrue(handler.handle_message(":Armandur!~Rasmus@localhost.ip INVITE BOT :#armandur_test"))

if __name__ == '__main__':
    unittest.main()
