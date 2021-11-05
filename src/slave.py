import os
import sys
import logging

from utils import open_pipe, OpenMode
from commands import Commands

logger = logging.getLogger()
commands_map = {
    'noop': Commands.NOOP,
    'user+pass': Commands.USER_PASS,
    'pass': Commands.PASS
}
COMMAND_PIPE_PATH = "/tmp/commands.pipe"


def slave(command):
    cmd = commands_map[command]
    pipe = open_pipe(COMMAND_PIPE_PATH, OpenMode.WRITE, blocking=False)
    if pipe:
        byte_cmd = cmd.value.to_bytes(1, 'big')
        os.write(pipe, byte_cmd)
        os.close(pipe)
        sys.exit(0)
    else:
        print("Botox is not running or is stopped")
        sys.exit(-1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Trigger botox')
    parser.add_argument('cmd', type=str, choices=['noop', 'user+pass', 'pass'],
                        help='command to send')
    args = parser.parse_args()
    slave(args.cmd)