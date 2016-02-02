from Flags import Flags
from mock import *
import handlers
import unittest


class TestAdminHandler(unittest.TestCase):
    def test_disconnect(self):
        flags = Flags()
        flags.setFlag('CHANNEL', 'TEST')
        flags.setFlag('IN_CHANNEL', True)
        flags.setFlag('NICK', 'BOT')
        flags.setFlag("ADMIN", "Armandur")
        flags.setFlag("CAN_QUIT", True)

        bot = DummyAdminBot(flags)
        handler = handlers.AdminHandler(bot, flags)

        handler.handle_message(":Armandur! BOT: quit")
        self.assertFalse(bot.connected)

    def test_reload(self):
        flags = Flags()
        flags.setFlag('CHANNEL', 'TEST')
        flags.setFlag('IN_CHANNEL', True)
        flags.setFlag('NICK', 'BOT')
        flags.setFlag("ADMIN", "Armandur")

        bot = DummyAdminBot(flags)
        handler = handlers.AdminHandler(bot, flags)

        handler.handle_message(":Armandur! BOT: reload")

    def test_count(self):
        flags = Flags()
        flags.setFlag('CHANNEL', 'TEST')
        flags.setFlag('IN_CHANNEL', True)
        flags.setFlag('NICK', 'BOT')
        flags.setFlag("ADMIN", "Armandur")

        bot = DummyAdminBot(flags)
        handler = handlers.AdminHandler(bot, flags)

        handler.handle_message(":Armandur! BOT: count")

    def test_list(self):
        flags = Flags()
        flags.setFlag('CHANNEL', 'TEST')
        flags.setFlag('IN_CHANNEL', True)
        flags.setFlag('NICK', 'BOT')
        flags.setFlag("ADMIN", "Armandur")

        bot = DummyAdminBot(flags)
        handler = handlers.AdminHandler(bot, flags)

        handler.handle_message(":Armandur! BOT: list")

    def test_raw(self):
        flags = Flags()
        flags.setFlag('CHANNEL', 'TEST')
        flags.setFlag('IN_CHANNEL', True)
        flags.setFlag('NICK', 'BOT')
        flags.setFlag("ADMIN", "Armandur")
        flags.setFlag("RAW_ENABLED", True)

        bot = DummyAdminBot(flags)
        handler = handlers.AdminHandler(bot, flags)

        bot.sock.connect(("irc.snoonet.org", 6667))

        handler.handle_message(":Armandur! BOT: raw QUIT")