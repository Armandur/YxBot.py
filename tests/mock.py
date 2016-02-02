import socket


class DummyBot:
    def __init__(self, flags):
        self.flags = flags

    def _nick(self):
        return self.flags.getFlag('NICK')


class DummyMessageAssertBot(DummyBot):
    def __init__(self, flags, test, assertMessage):
        self.assertMessage = assertMessage
        self.test = test

    def send(self, message):
        self.test.assertEqual(message, self.assertMessage)


class DummyNicklistBot(DummyBot):
    nicklist = set()

    def _getNicks(self):
        pass


class DummyAdminBot(DummyBot):
    yxfabrikat = set()
    yxtyp = set()
    kroppsdel = set()

    def __init__(self, flags):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = True
        self.flags = flags

    def disconnect(self):
        self.connected = False

    def _load(self):
        pass

    def _sendMessage(self, msg):
        pass
