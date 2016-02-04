#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MessageHandler import MessageHandler
import random


class AxeHandler(MessageHandler):
    def handle_message(self, message):
        if message.find("PRIVMSG") != -1 and (message.find(" :!yxa") != -1 or message.find(" :.yxa") != -1):
            splitted = message[message.find(" :!yxa"):].split()

            print splitted

            if len(splitted) == 2:
                nick = splitted[1]
                if self.flags.getFlag("USERS_ONLY"):
                    if nick in self.bot.nicklist:
                        self.bot._sendMessage(self.yxa(splitted[1]), True)
                    else:
                        self.bot._sendMessage("Ursäkta, vem då?")
                else:
                    self.bot._sendMessage(self.yxa(splitted[1]), True)

    def yxa(self, nick):
        print "-- Yxar " + nick + " --"
        fab = random.sample(self.bot.yxfabrikat, 1)[0]
        typ = random.sample(self.bot.yxtyp, 1)[0]
        krp = random.sample(self.bot.kroppsdel, 1)[0]

        s = "tar en " + typ + " tillverkad av " + fab + " och hugger den i " + krp + " på " + nick + ".\n"

        return s
