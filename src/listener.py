from threading import Thread, Event
import os
import select
import logging

from commands import Commands
from executor import Executor
from utils import open_pipe, OpenMode

logger = logging.getLogger(__name__)


class Listener(Thread):
    def __init__(self, control_pipe, command_pipe, executor, *args, **kwargs):
        super(Listener, self).__init__(*args, **kwargs)
        self.control_pipe_path = control_pipe
        self.command_pipe_path = command_pipe
        self.control_pipe = None
        self.command_pipe = None
        self._stop_event = Event()
        self.executor = executor

    def run(self):
        self.control_pipe = open_pipe(self.control_pipe_path, OpenMode.READ, blocking=True)
        self.command_pipe = open_pipe(self.command_pipe_path, OpenMode.READ)
        stopped = False
        while True and not stopped:
            ready_read, _, _ = select.select([self.command_pipe, self.control_pipe], [], [])
            for fd in ready_read:

                cmd_byte = os.read(fd, 1)
                if fd == self.command_pipe:
                    if len(cmd_byte) == 0:
                        continue
                    else:

                        cmd = int.from_bytes(cmd_byte, 'big')
                        cmd = Commands(cmd)
                        logger.debug(f"processing command {cmd}")
                        if cmd is Commands.NOOP:
                            pass
                        elif cmd is Commands.USER_PASS:
                            self.executor.set_user_pass()
                        elif cmd is Commands.PASS:
                            self.executor.set_pass()
                        else:
                            logger.warning(f"Unrecognized command {cmd}")

                if fd == self.control_pipe:
                    logger.debug(f"asking control {cmd_byte}")
                    self.clean()
                    stopped = True
                    break

    def clean(self):
        os.close(self.control_pipe)
        os.close(self.command_pipe)
        logger.debug("Cleaned")
