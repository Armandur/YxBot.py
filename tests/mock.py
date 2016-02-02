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
        self.test.assertEqual(message, assertMessage)
