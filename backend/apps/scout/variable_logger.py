import logging
import collections

"""
Logger that stores results in a collection. Based on: https://stackoverflow.com/a/37967421
"""


class VariableLogHandler(logging.Handler):

    def __init__(self, log_queue):
        logging.Handler.__init__(self)
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.append({"code": record.levelno, "type": record.levelname.lower(), "message": self.format(record)})


class VariableLogger(object):

    def __init__(self, max_len: int):
        self._log_queue = collections.deque(maxlen=max_len)
        self._log_handler = VariableLogHandler(self._log_queue)

    def contents(self):
        return list(self._log_queue)

    @property
    def log_handler(self):
        return self._log_handler
