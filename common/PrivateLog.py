
# encoding=utf-8

import logging
import logging.handlers

class Log(object):
    def __init__(self, _level='INF', _filename = '', _is_stream = False):

        self.logger = logging.getLogger('PrivateLog')

        formatter = logging.Formatter('%(asctime)s %(levelname)s| %(filename)s:%(lineno)s %(message)s')
        #formatter = logging.Formatter('%(asctime)s %(levelname)s| %(message)s')

        if _filename:
            max_file_size = 1024 * 1024 * 100
            file_handler = logging.handlers.RotatingFileHandler(_filename, maxBytes=max_file_size, backupCount=10)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if _is_stream or not _filename:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

        if _level == 'DEB':
            self.logger.setLevel(logging.DEBUG)
        elif _level == 'WRN':
            self.logger.setLevel(logging.WARNING)
        else:
            self.logger.setLevel(logging.INFO)

    def get(self):
        return self.logger
