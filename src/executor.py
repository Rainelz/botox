import logging
from pynput.keyboard import Controller, Key
logger = logging.getLogger('pynput')
logger.handlers = None

from crypto import Crypto

logger = logging.getLogger(__name__)


class Executor:
    def __init__(self, key):
        self.key = key
        self.crypto = Crypto()
        with open('resources/.botox', 'rb') as f:
            self.data = f.read()
        self.keyboard = Controller()

    def set_user_pass(self):
        logger.debug("Executing commands user")
        self.keyboard.type(self.crypto.decrypt(self.data, self.key)['username'])
        self.keyboard.tap(Key.tab)
        self.set_pass()

    def set_pass(self):
        logger.debug("Executing commands password ")
        self.keyboard.type(self.crypto.decrypt(self.data, self.key)['password'])
        self.keyboard.tap(Key.enter)
