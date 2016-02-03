#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Flags import Flags
from mock import *
import handlers
import unittest


class TestAxeHandler(unittest.TestCase):
    def test_axe(self):
        flags = Flags()
        flags.setFlag("USERS_ONLY", False)

        bot = DummyAxeBot(flags)

        bot.yxfabrikat = set(["Wetterlings"])
        bot.yxtyp = set(["bredyxa"])
        bot.kroppsdel = set(["ryggen"])

        print str(bot.yxfabrikat) + str(bot.yxtyp) + str(bot.kroppsdel)

        bot.nicklist = set(["User"])

        handler = handlers.AxeHandler(bot, flags)

        target = "User"

        handler.handle_message("PRIVMSG :!yxa " + target)

        flags.setFlag("USERS_ONLY", True)

        handler.handle_message("PRIVMSG :!yxa " + target)

        expected = "tar en bredyxa tillverkad av Wetterlings och hugger den i ryggen på " + target + ".\n"

        self.assertEqual(expected, handler.yxa(target))

if __name__ == '__main__':
    unittest.main()
