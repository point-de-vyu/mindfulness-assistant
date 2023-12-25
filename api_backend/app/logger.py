import logging
import sys

main_logger = logging.getLogger(__name__)
main_logger.setLevel(logging.DEBUG)


def set_up_logger(set_up_stdout: bool = True, set_up_file: bool = False) -> logging.Logger:
    global main_logger
    main_logger.handlers = []
    formatter = logging.Formatter("[%(asctime)s] !%(name)s! ->%(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
    if set_up_stdout:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        main_logger.addHandler(console_handler)
    return main_logger


def get_logger() -> logging.Logger:
    global main_logger
    return main_logger


