#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, random, time


class YxBot:
	#yxfabrikat = ["Gränsfors Bruk", "Wetterlings", "Husqvarna", "Hjärtum", "Billnäs Bruk", "Jonsered", "Stihl", "John Neeman", "Hultafors", "Säter", "Collins", "Council Tool", "Estwing"]
	#yxtyp = ["amerikansk ", "svensknackad ", "vikinga", "japansk ", "finsk ", "norsk ", "dubbeleggad ", "skarv", "knut","tjäckel", "skräd", "snickar", "klyv"]
	#kroppsdel = ["huvudet", "benet", "bröstet", "högerarmen", "vänsterarmen", "högerbenet", "vänsterbenet", "skrevet", "axeln", "ryggen", "magen", "låret"]

	yxfabrikat = []
	yxtyp = []
	kroppsdel = []

	connection = ()

	def __init__(self, conn, chan, nick, admin, paths, sil=False):
		self.nick = nick
		self.connection = conn
		self.channel = chan
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.running = True
		self.adminNick = admin
		self.silent = sil
		self.paths = paths
		self._load(paths)

	def _load(self, paths):

		print "-- Loading configuration from "
		print paths

		self.yxfabrikat = open(paths[0]).read().split('\n')
		self.yxtyp = open(paths[1]).read().split('\n')
		self.kroppsdel = open(paths[2]).read().split('\n')

		print self.yxfabrikat
		print self.yxtyp
		print self.kroppsdel
		print self._yxa("test")

	def connect(self):
		self.sock.connect(self.connection)
		self._receivingLoop()

	def disconnect(self):
		self.sock.send("QUIT\n")
		self.running = False

	def _register(self):
		print "-- Registering with " + self.nick + " --\n"

		self.sock.send("USER " + self.nick + " . . :Detta är " + self.nick + "\n"
					  +"NICK " + self.nick + "\n")
		
		return

	def _joinChannel(self):
		print "-- Joining channel " + self.channel + " --\n"
		self.sock.send("JOIN " + self.channel + "\n")

	def _sendMessage(self, message, action=False):
		if self.silent:
			param = "Armandur"
		else:
			param = self.channel

		if not action:
			compiled = "PRIVMSG " + param + " :" + message + "\n"
		else:
			compiled = "PRIVMSG " + param + " :"+"\x01"+"ACTION " + message + "\n"

		print "-- sending Message " + compiled

		self.sock.send(compiled)


	def _pong(self, ping):
		print "-- Answering PING with PONG :" + ping + " --\n"
		self.sock.send("PONG :" + ping + "\n")

	def _handleMessage(self, message):
		if message.find("PING :") != -1:
			ping = message.split();
			ping = ping[1]
			ping = ping[1:]

			self._pong(ping)
		if message.find(":"+self.adminNick+"!") != -1:
			if message.find(self.nick + ": quit") != -1:
				self.disconnect()
			if message.find(self.nick + ": reload") != -1:
				self._load(self.paths)

		if message.find("Closing link") != -1 and message.find(self.nick) != -1:
			self.disconnect();

		if message.find("PRIVMSG") != -1 and message.find(" :!yxa") != -1:

			index = message.find(" :!yxa")
			formatted = message[index:]
			splitted = formatted.split()
			length = len(splitted)

			print splitted

			if length == 2:
				self._sendMessage(self._yxa(splitted[1]), True)

	def _yxa(self, nick):
		print "-- Yxar " + nick + " --"
		fab = random.choice(self.yxfabrikat)
		typ = random.choice(self.yxtyp)
		krp = random.choice(self.kroppsdel)

		s = "tar en " + typ + " tillverkad av " + fab + " och hugger den i " + krp + " på " + nick + ".\n"

		return s

	def _receivingLoop(self):

		time.sleep(3)

		registered = False
		joined = False

		while self.running:
			ircmsg = self.sock.recv(2048)
			ircmsg = ircmsg.strip("\n\r")
			print ircmsg

			if not registered:
				self._register()
				registered = True

			if not joined and ircmsg.find("MODE " + self.nick + " +") != -1:
				time.sleep(3)
				self._joinChannel()
				joined = True

			self._handleMessage(ircmsg)

		print "-- Loop stopped -- \n"

random.seed()
bot = YxBot(("irc.snoonet.org", 6667), "#sweden", "YxBot", "Armandur", ["yxfabrikat.txt", "yxtyp.txt", "kroppsdel.txt"])
bot.connect()