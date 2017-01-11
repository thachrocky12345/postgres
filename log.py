from datetime import datetime

from logging import (
    Formatter,
    getLogger,
    StreamHandler,
    FileHandler,
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    WARNING
)
import os
from socket import gethostname

LOG_DIRECTORY = '/opt/farmobile/logs'
LOG_FILE_NAME = '{host_name}_{process_name}_{exec_timestamp}_{process_id}.log'
LOG_LEVELS = frozenset([DEBUG, ERROR, FATAL, INFO, WARNING])

log_msg_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class LoggingSetup(object):
    setup_logger = getLogger()

    def __init__(self, process_name, subdirectory=None, daily_file=False, console_level=None, file_level=None):
        self.file_log_level = file_level
        self.console_log_level = console_level
        self.subdirectory = subdirectory
        self.process_name = process_name
        self.daily_file = daily_file

        self.log_file_name = self._determine_log_file_name()
        self.log_file_dir = self._determine_log_file_dir()
        self.log_file_mode = self._determine_log_file_mode()
        self.log_file_path = os.path.join(self.log_file_dir, self.log_file_name)

    def _determine_log_file_name(self):
        if self.daily_file:
            log_file_ts = datetime.now().strftime('%Y%m%d')
        else:
            log_file_ts = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Assuming a "<hostname>.farmobile.local" return value from gethostname(),
        # we only need the first part.
        short_host_name = gethostname().split('.')[0]
        log_file_name = LOG_FILE_NAME.format(
            host_name=short_host_name,
            process_name=self.process_name,
            exec_timestamp=log_file_ts,
            process_id=os.getpid()
        )

        return log_file_name

    def _determine_log_file_mode(self):
        if self.daily_file:
            log_file_mode = 'a'
        else:
            log_file_mode = 'w'

        return log_file_mode

    def _determine_log_file_dir(self):
        if self.subdirectory is None:
            log_file_dir = LOG_DIRECTORY
        else:
            log_file_dir = os.path.join(LOG_DIRECTORY, self.subdirectory)

        if not os.path.exists(log_file_dir):
            os.makedirs(log_file_dir)

        return log_file_dir

    def _setup_file_handler(self):
        file_handler = FileHandler(self.log_file_path, mode=self.log_file_mode)
        file_handler.setLevel(self.file_log_level)
        file_handler.setFormatter(log_msg_format)

        return file_handler

    def _setup_console_handler(self):
        console_handler = StreamHandler()
        console_handler.setLevel(self.console_log_level)
        console_handler.setFormatter(log_msg_format)

        return console_handler

    def _validate_log_levels(self):
        invalid_log_levels = []
        if self.file_log_level is None and self.console_log_level is None:
            raise ValueError("At least one of the file and console levels must me set")
        if self.file_log_level is not None and self.file_log_level not in LOG_LEVELS:
            invalid_log_levels.append('file')
        if self.console_log_level is not None and self.console_log_level not in LOG_LEVELS:
            invalid_log_levels.append('console')

        if invalid_log_levels:
            err_msg = (
                'and '.join(invalid_log_levels) +
                ' log level invalid - valid values are None or a log '
                'level as defined in the built-in logging module'
            )
            raise ValueError(err_msg)

    def init_logging(self):
        self._validate_log_levels()

        if self.file_log_level is None:
            log_level = self.console_log_level
        elif self.console_log_level is None:
            log_level = self.file_log_level
        else:
            log_level = min(self.file_log_level, self.console_log_level)
        self.setup_logger.setLevel(log_level)

        if self.console_log_level is not None:
            console_handler = self._setup_console_handler()
            self.setup_logger.addHandler(console_handler)

        if self.file_log_level is not None:
            file_handler = self._setup_file_handler()
            self.setup_logger.addHandler(file_handler)

        print "Log file: {}/{}".format(self.log_file_dir,
                                       self.log_file_name)
