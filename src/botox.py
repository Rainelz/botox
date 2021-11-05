from multiprocessing import Queue

import rumps
import os

from gui import CredentialsGUI, PasswordGUI
from crypto import Crypto
from executor import Executor, check_permissions
from listener import Listener
import logging
import sys
from pathlib import Path

from utils import open_pipe, OpenMode
from slave import slave


def config_logger(out_dir=None, step=''):
    logger = logging.getLogger()
    if not len(logger.handlers):
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s - [%(process)s] %(message)s')
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        stdout_handler.setLevel(logging.DEBUG)
        if out_dir:
            out_dir = Path(out_dir) / 'logs'
            out_dir.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(f'{out_dir}/botox.log')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            logger.addHandler(file_handler)
            file_handler = logging.FileHandler(f'{out_dir}/botox_debug.log')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            logger.addHandler(file_handler)
        logger.addHandler(stdout_handler)

    return logger


logger = config_logger(Path.home() / 'Library' / 'Application Support' / 'Botox')
rumps.debug_mode(True)

CONTROL_PIPE_PATH = '/tmp/control.pipe'
COMMAND_PIPE_PATH = "/tmp/commands.pipe"


class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("💉", quit_button=None)

        self.listener = None
        self.listening = False
        self.control_pipe = None
        self.data_file = Path('resources') / '.botox'

        self._cleanup_fifos()
        self.crypto = Crypto()
        self.key = None
        self.menu = [rumps.MenuItem("Start", callback=self.start), rumps.MenuItem("Stop", callback=None),
                     rumps.MenuItem("Set Credentials", callback=self.set_credentials)]

    def _cleanup_fifos(self):
        control = Path(CONTROL_PIPE_PATH)
        commands = Path(COMMAND_PIPE_PATH)
        control.unlink(missing_ok=True)
        commands.unlink(missing_ok=True)

    def _store_data(self, data):
        with open(self.data_file, 'wb') as f:
            f.write(data)

    @rumps.clicked("Set Credentials")
    def set_credentials(self, _):
        logger.debug("BOTOX - Set Credentials")
        dataQ = Queue()

        gui = CredentialsGUI(dataQ)
        gui.start()
        gui.join()

        data = dataQ.get(block=False)
        if data:
            data, key = self.crypto.encrypt(data)
            self._store_data(data)
            self.key = key
            return True
        return False

    def set_key(self):
        logger.debug("BOTOX - Set Key")

        dataQ = Queue()

        gui = PasswordGUI(dataQ)
        gui.start()
        gui.join()
        key = dataQ.get(block=False)
        if key:
            self.key = key
            return True
        return False

    def start(self, sender):
        logger.debug("BOTOX - Start")
        if not check_permissions():
            rumps.notification('WARNING', 'Please give Botox permissions from settings', '')

        if not self.data_file.exists():
            if not self.set_credentials(None):
                logger.debug("Dismissed Credentials insert")
                return
        elif not self.key:
            if not self.set_key():
                logger.debug("Dismissed Password insert")
                return

        executor = Executor(self.data_file, self.key)
        self.listener = Listener(CONTROL_PIPE_PATH, COMMAND_PIPE_PATH, executor)
        self.listener.start()
        self.listening = True
        self.control_pipe = open_pipe(CONTROL_PIPE_PATH, OpenMode.WRITE, blocking=True)
        logger.info("BOTOX - Started")
        self.title = '🩺'
        sender.set_callback(None)
        menu_item = self.menu['Stop']
        if menu_item.callback is None:
            menu_item.set_callback(self.stop)

    def stop_listener(self):

        if self.control_pipe:
            try:
                os.write(self.control_pipe, b'a')
                logger.debug("Sent stop command")

            except BrokenPipeError as e:
                logger.debug("Control pipe already closed")

        if self.listener and self.listener.is_alive():
            self.listener.join()
            logger.debug("Listener joined")

    def cleanup(self):
        if self.control_pipe:
            os.close(self.control_pipe)

    def stop(self, _):
        menu_item = self.menu['Start']
        self.stop_listener()

        self.title = "💉"
        if menu_item.callback is None:
            menu_item.set_callback(self.start)

    @rumps.clicked("Quit")
    def quit_application(self, _):
        self.stop_listener()
        self.cleanup()

        logger.debug("Cleanup complete - Exiting")
        rumps.quit_application()


def main(args):
    if args.cmd:
        slave(args.cmd)
    else:
        AwesomeStatusBarApp().run()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Trigger botox')
    parser.add_argument('--cmd', type=str, required=False, choices=['noop', 'user+pass', 'pass'],
                        help='command to send')
    args = parser.parse_args()
    main(args)
