from Flags import Flags
from mock import *
import handlers
import unittest

class TestPingHandler(unittest.TestCase):

  def test_ping(self):
      bot = DummyMessageAssertBot(Flags(), self, 'PING')
      handler = handlers.PingHandler(bot, None)
      handler.handle_message('PING')

if __name__ == '__main__':
    unittest.main()
