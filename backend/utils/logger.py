import logging
import os

LOG_LEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()

class Log:

    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s %(message)s', 
            level=LOG_LEVEL,
            datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        self.logger = logging.getLogger()


    def i(self, message: str):
        self.logger.info(message)

    def d(self, message: str):
        self.logger.debug(message)