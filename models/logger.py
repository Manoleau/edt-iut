import logging


class Logger:
    def __init__(self, nom):
        self.logger = logging.getLogger(nom)

    def ecrire_info(self, message):
        self.logger.info(message)

    def ecrire_waring(self, message):
        self.logger.warning(message)

    def ecrire_error(self, message):
        self.logger.error(message)
