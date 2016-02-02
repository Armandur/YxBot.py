from Flags import Flags
from mock import *
import handlers
import unittest

class TestKickedHandler(unittest.TestCase):

  def test_kicked(self):
      flags = Flags()
      flags.setFlag('CHANNEL', 'TEST')
      flags.setFlag('IN_CHANNEL', True)
      flags.setFlag('NICK', 'BOT')
      bot = DummyBot(flags)
      handler = handlers.KickedHandler(bot, flags)
      handler.handle_message('KICK TEST BOT')
      self.assertFalse(flags.getFlag('IN_CHANNEL'))

if __name__ == '__main__':
    unittest.main()
