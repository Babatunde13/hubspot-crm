from logging import getLogger, StreamHandler, Formatter, DEBUG

class Logger:
    def __init__(self, name):
        self.logger = getLogger(name)
        self.logger.setLevel(DEBUG)
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        json_formatter = Formatter(
            '{"timestamp": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s", "filename": "%(filename)s", "lineno": %(lineno)d, "funcName": "%(funcName)s", "context": %(context)s}'
        )
        handler.setFormatter(json_formatter)
        handler.set_name(name)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger
    
    def log(self, level, message, data=None):
        self.logger.log(level, message, extra={"context": data})

    def error(self, message, context=None):
        self.logger.error(message, extra={"context": context})

    def info(self, message, context=None):
        self.logger.info(message, extra={"context": context})

    def debug(self, message, context=None):
        self.logger.debug(message, extra={"context": context})

    def warning(self, message, context=None):
        self.logger.warning(message, extra={"context": context})
