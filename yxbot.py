#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, random, time, Flags, ConfigParser

from handlers import PingHandler
from handlers import KickedHandler
from handlers import InviteHandler
from handlers import NicklistHandler
from handlers import AdminHandler
from handlers import FlagEditHandler
from handlers import AxeHandler

class YxBot:
	yxfabrikat = set()
	yxtyp = set()
	kroppsdel = set()

	nicklist = set()

	flags = Flags.Flags()

	connection = ()

	nickListBuffer = ""

	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.running = True

		# Default flags
		self.flags.setFlag("CAN_QUIT", False)
		self.flags.setFlag("RAW_ENABLED", False)
		self.flags.setFlag("IN_CHANNEL", False)

		self._load()
		self._init_handlers()

	def _init_handlers(self):
		self.handlers = [
			KickedHandler(self, self.flags),
			PingHandler(self, self.flags),
			InviteHandler(self, self.flags),
			NicklistHandler(self, self.flags),
			AdminHandler(self, self.flags),
			FlagEditHandler(self, self.flags),
			AxeHandler(self, self.flags)
		]

	def _load(self):

		config = ConfigParser.ConfigParser()
		config.read("config.cfg")

		print "-- Reading configuration file config.cfg --\n"

		#Read connection settings from config-file
		self.flags.setFlag("CONNECTION", (config.get("conn", "server"), config.get("conn", "port")))
		self.flags.setFlag("CHANNEL", config.get("conn", "channel"))
		self.flags.setFlag("NICK", config.get("conn", "nick"))

		#Read configuration settings from config-file
		self.flags.setFlag("ADMIN", config.get("conf", "admin"))
		self.flags.setFlag("USERS_ONLY", config.get("conf", "users_only"))

		#Read paths from config-file
		self.flags.setFlag("PATHS", [config.get("paths", "fabp"), config.get("paths", "axep"), config.get("paths", "bodp")])

		paths = self.flags.getFlag("PATHS")

		print "-- Loading configuration from "
		print paths
		print "\n"

		sets = [set(), set(), set()]

		i = 0
		for path in paths:
			f = open(path)
			for l in f:
				if l not in sets[i]:
					sets[i].add(l.strip('\n'))
			f.close()
			i += 1

		self.yxfabrikat = sets[0]
		self.yxtyp = sets[1]
		self.kroppsdel = sets[2]

		print self.yxfabrikat
		print self.yxtyp
		print self.kroppsdel

		print AxeHandler(self, self.flags).yxa("test")

	def _nick(self):
		return str(self.flags.getFlag("NICK"))

	def _channel(self):
		return str(self.flags.getFlag("CHANNEL"))

	def connect(self):
		self.sock.connect(self.flags.getFlag("CONNECTION"))
		self._receivingLoop()

	def disconnect(self):
		self.sock.send("QUIT\n")
		self.running = False

	def send(self, message):
		self.sock.send(message)

	def _register(self):
		print "-- Registering with " + self._nick() + " --\n"

		self.sock.send("USER " + self._nick() + " . . :Detta är " + self._nick() + "\n"
					 + "NICK " + self._nick() + "\n")

	def _joinChannel(self):
		if not self.flags.getFlag("IN_CHANNEL"):
			print "-- Joining channel " + self._channel() + " --\n"
			self.sock.send("JOIN " + self._channel() + "\n")
			self.flags.setFlag("IN_CHANNEL", True)
		else:
			print "-- Already in Channel --\n"

	def _leaveChannel(self):
		if self.flags.getFlag("IN_CHANNEL"):
			print "-- Leaving channel --\n"
			self.sock.send("PART\n")
		else:
			print "-- Not in channel --\n"

	def _changeChannel(self, chan):
		print "-- Changing channel flag to " + chan + " --\n"
		self.flags.setFlag("CHANNEL", chan)

	def _sendMessage(self, message, action=False):
		if self.flags.getFlag("SILENT"):
			param = self.flags.getFlag("ADMIN")
		else:
			param = self._channel()

		if not action:
			compiled = "PRIVMSG " + param + " :" + message + "\n"
		else:
			compiled = "PRIVMSG " + param + " :" + "\x01" + "ACTION " + message + "\n"

		print "-- sending Message " + compiled.strip("\n") + " --\n"

		self.sock.send(compiled)

	def _getNicks(self):
		print "-- Sending NAMES command --\n"
		self.sock.send("NAMES " + self.flags.getFlag("CHANNEL") + "\n")

	def _handleMessage(self, message):
		for handler in self.handlers:
			handler.handle_message(message)

		if message.find("Closing link") != -1 and message.find(self._nick()) != -1:
			self.disconnect()

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

					if not joined and buff.find("MODE " + self._nick()) != -1:
						self._joinChannel()
						joined = True
					buff = ""

		print "-- Loop stopped -- \n"
