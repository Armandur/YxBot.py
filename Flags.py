class Flags:
	_flags = {}

	def __init__(self):
		self._flags["INIT"] = True

	def setFlag(self, flag, value):
		self._flags[flag] = value

	def getFlag(self, flag):
		if flag in self._flags:
			return self._flags[flag]
		else:
			print "##FLAG NOT IN DICT##\n"
			return False

	def removeFlag(self, flag):
		if flag in self._flags:
			del self._flags[flag]
		else:
			print "##FLAG NOT PRESENT##"
