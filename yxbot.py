#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, random, time

class YxBot:
	yxfabrikat = []
	yxtyp = []
	kroppsdel = []
	nickList = []

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

		print "-- sending Message " + compiled.strip("\n") + " --\n"

		self.sock.send(compiled)

	def _getNicks(self):
		print "-- Sending NAMES command --\n"
		self.sock.send("NAMES\n")

	def _updateNicklist(self, message):
		print "-- Updating NickList --\n"
		self.nickList = []
		index = message.find(":"+self.nick)
		text = message[index + 1:]
		text = text.split()
		self.nickList = text

		print "NickList contains: "
		print self.nickList

	def _pong(self, ping):
		print "-- Answering PING with PONG :" + ping + " --\n"
		self.sock.send("PONG :" + ping + "\n")

	def _handleMessage(self, message):
		if message.find("PING :") != -1:
			ping = message.split();
			ping = ping[1]
			ping = ping[1:]

			self._pong(ping)

		if message.find("PART") != -1 or message.find("JOIN") != -1:
			self._getNicks()

		if message.find("353") != -1 and message.find(self.nick) != -1:
			self._updateNicklist(message)

		if message.find(":"+self.adminNick+"!") != -1:
			#if message.find(self.nick + ": quit") != -1:
			#	self.disconnect()
			if message.find(self.nick + ": reload") != -1:
				self._load(self.paths)
			if message.find(self.nick + ": count") != -1:
				text = "Fabrikat: " + str(len(self.yxfabrikat)) + ", Typer: " + str(len(self.yxtyp)) + ", Kroppsdelar: " + str(len(self.kroppsdel))
				self._sendMessage(text)

		if message.find("Closing link") != -1 and message.find(self.nick) != -1:
			self.disconnect();

		if message.find("PRIVMSG") != -1 and message.find(" :!yxa") != -1:
			index = message.find(" :!yxa")
			formatted = message[index:]
			splitted = formatted.split()

			print splitted

			if len(splitted) == 2:
				nick = splitted[1]
				if self._onlyUsersInChannel:
					if nick in self.nickList:
						self._sendMessage(self._yxa(splitted[1]), True)
					else:
						self._sendMessage("Ursäkta, vem då?")
				else:
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

		buff = ""

		while self.running:
			for c in self.sock.recv(2048):
				if c != "\n":
					buff += c
				else:
					print buff

					self._handleMessage(buff)

					if not registered:
						self._register()
						registered = True

					if not joined and buff.find("MODE " + self.nick) != -1:
						self._joinChannel()
						joined = True
						self._getNicks()

					buff = ""

		print "-- Loop stopped -- \n"

random.seed()
#bot = YxBot(("irc.snoonet.org", 6667), "#sweden", "YxBot", "Armandur", ["yxfabrikat.txt", "yxtyp.txt", "kroppsdel.txt"])
bot = YxBot(("portlane.se.quakenet.org", 6667), "#anrop.net", "Yxbotten", "Armandur", ["yxfabrikat.txt", "yxtyp.txt", "kroppsdel.txt"])
#bot = YxBot(("irc.oftc.net", 6667), "#devscout", "YxBot", "Armandur", ["yxfabrikat.txt", "yxtyp.txt", "kroppsdel.txt"])
bot.connect()