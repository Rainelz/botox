import os, errno
import sys
import logging
logger = logging.getLogger(__name__)
from enum import Enum, auto
class OpenMode(Enum):
    READ = auto()
    WRITE = auto()

def open_pipe(pipe_path: str, mode:OpenMode, blocking=False):
    non_block_flag = 0 if blocking else os.O_NONBLOCK
    mode_flag = os.O_RDONLY if mode is OpenMode.READ else os.O_WRONLY
    try:
        os.mkfifo(pipe_path)
    except FileExistsError as e:
        pass
    except Exception as e:
        logger.error(f"Cannot create {pipe_path} pipe", e)
        sys.exit()

    try:
        pipe_fd = os.open(pipe_path, mode_flag | non_block_flag)
        return pipe_fd
    except OSError as ex:
        logger.exception(f"Cannot open {pipe_path}, in mode {mode} + {blocking=}")

    except Exception as e:
        logger.exception(e)
        sys.exit(1)