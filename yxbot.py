#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, random, time, Flags

from handlers import PingHandler
from handlers import KickedHandler
from handlers import InviteHandler
from handlers import NicklistHandler

class YxBot:
	yxfabrikat = set()
	yxtyp = set()
	kroppsdel = set()
	nicklist = set()

	flags = Flags.Flags()

	connection = ()

	nickListBuffer = ""

	def __init__(self, flags):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.running = True

		# Default flags
		self.flags.setFlag("CAN_QUIT", False)
		self.flags.setFlag("RAW_ENABLED", False)
		self.flags.setFlag("IN_CHANNEL", False)

		# Update flags based on user flags
		self.flags._flags.update(flags._flags)


		self._initHandlers()
		self._load()

	def _init_handlers(self):
		self.handlers = [
			KickedHandler(self, self.flags),
			PingHandler(self, self.flags),
			InviteHandler(self, self.flags),
			NicklistHandler(self, self.flags)
		]

	def _load(self):
		paths = self.flags.getFlag("PATHS")

		print "-- Loading configuration from "
		print paths

		self.yxfabrikat = open(paths[0]).read().split('\n')
		self.yxtyp = open(paths[1]).read().split('\n')
		self.kroppsdel = open(paths[2]).read().split('\n')

		print self.yxfabrikat
		print self.yxtyp
		print self.kroppsdel
		print self._yxa("test")

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

		#ONLY ADMIN NICK SHOULD BE ABLE TO USE

		if message.find(":" + self.flags.getFlag("ADMIN") + "!") != -1:
			if message.find(self._nick() + ": quit") != -1 and self.flags.getFlag("CAN_QUIT"):
				self.disconnect()

			if message.find(self._nick() + ": reload") != -1:
				self._load()

			if message.find(self._nick() + ": count") != -1:
				self._sendMessage("Fabrikat: " + str(len(self.yxfabrikat)) + ", Typer: " + str(len(self.yxtyp)) + ", Kroppsdelar: " + str(len(self.kroppsdel)))

			if message.find(self._nick() + ": list") != -1:
				self._sendMessage("Fabrikat: " + str(self.yxfabrikat) + ", Typer: " + str(self.yxtyp) + ", Kroppsdelar: " + str(self.kroppsdel) + "\n")

			if message.find(self._nick() + ": raw") != -1 and self.flags.getFlag("RAW_ENABLED"):
				text = message[message.find(": raw"):]
				text = text.split(": raw")
				text = text[1:]

				self.sock.send(text[0].strip() + "\n")

			#EDITING FLAGS FROM CHAT
			if message.find(self._nick() + ": setFlag") != -1 or message.find(self._nick() + ": getFlag") != -1 or message.find(self._nick() + ": delFlag") != -1:
				print "-- EDITING FLAGS FROM CHAT --\n"

				if message.find(self._nick() + ": setFlag") != -1:
					print "-- SET FLAG --\n"
					splitted = message[message.find("setFlag"):].split()

					if len(splitted) == 4: #1 setFlag, 2 flag, 3 type, 4 value ex, setFlag SILENT BOOL True => ['setFlag', 'SILENT', 'BOOL', 'True']
						if splitted[2] == "STR":
							self.flags.setFlag(splitted[1], splitted[3])
						elif splitted[2] == "NUM":
							value = -1
							try:
								value = int(splitted[3])
							except ValueError:
								value = -1

							self.flags.setFlag(splitted[1], value)
						elif splitted[2] == "BOOL":
							value = False
							if splitted[3] == "True":
								value = True
							self.flags.setFlag(splitted[1], value)

				if message.find(self._nick() + ": getFlag") != -1:
					print "-- GET FLAG --\n"
					splitted = message[message.find("getFlag"):].split()

					if len(splitted) == 2: #1 getFlag, 2 flag
						self._sendMessage(splitted[1] + " : " + str(self.flags.getFlag(splitted[1])))

					print self.flags._flags

				if message.find(self._nick() + ": delFlag") != -1:
					print "-- DEL FLAG --\n"
					splitted = message[message.find("delFlag"):].split()

					if len(splitted) == 2: #1 delFlag, 2 flag
						self.flags.removeFlag(splitted[1])
			#END EDIT FLAGS
		#END ADMIN COMMANDS

		if message.find("Closing link") != -1 and message.find(self._nick()) != -1:
			self.disconnect()

		if message.find("PRIVMSG") != -1 and message.find(" :!yxa") != -1:
			splitted = message[message.find(" :!yxa"):].split()

			print splitted

			if len(splitted) == 2:
				nick = splitted[1]
				if self.flags.getFlag("USERS_ONLY"):
					if nick in self.nicklist:
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

					if not joined and buff.find("MODE " + self._nick()) != -1:
						self._joinChannel()
						joined = True
					buff = ""

		print "-- Loop stopped -- \n"
