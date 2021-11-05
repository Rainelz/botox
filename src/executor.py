import pyautogui
import logging

logger = logging.getLogger('pyautogui')
logger.handlers = None

from crypto import Crypto

logger = logging.getLogger(__name__)


class Executor:
    def __init__(self, key):
        self.key = key
        self.crypto = Crypto()
        with open('resources/.botox', 'rb') as f:
            self.data = f.read()

    def set_user_pass(self):
        logger.debug("Executing commands user")
        pyautogui.write(self.crypto.decrypt(self.data, self.key)['username'])
        pyautogui.press('tab')
        self.set_pass()

    def set_pass(self):
        logger.debug("Executing commands password ")
        pyautogui.write(self.crypto.decrypt(self.data, self.key)['password'])
        pyautogui.press('enter')
