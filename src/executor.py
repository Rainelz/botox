import logging
import HIServices
from pathlib import Path
from pynput.keyboard import Controller, Key
logger = logging.getLogger('pynput')
logger.handlers = None

from crypto import Crypto

logger = logging.getLogger(__name__)


def check_permissions():
    if not HIServices.AXIsProcessTrusted():
        test_input()
        return False
    return True


def test_input():
    Controller().tap(Key.alt)


class Executor:
    def __init__(self, file: Path, key):
        self.key = key
        self.crypto = Crypto()
        self.data = None
        if file.exists():
            with open(file, 'rb') as f:
                self.data = f.read()
        else:
            logger.warning("Can't find credentials data")
        self.keyboard = Controller()

    def set_user_pass(self):
        if self.data and self.key:
            logger.debug("Executing commands user")
            self.keyboard.type(self.crypto.decrypt(self.data, self.key)['username'])
            self.keyboard.tap(Key.tab)
            self.set_pass()
        else:
            logger.debug("Skipping command USER")

    def set_pass(self):
        if self.data and self.key:
            logger.debug("Executing commands password ")
            self.keyboard.type(self.crypto.decrypt(self.data, self.key)['password'])
            self.keyboard.tap(Key.enter)
        else:
            logger.debug("Skipping command PASS")
