from config.Configuration import Configuration

import logging


class LoggingConfiguration(Configuration):
    """
    Author: Ronny Friedland

    Handles logging configuration
    """

    CONFIG_DEFAULTS = {'loglevel':'INFO'}

    def __init__(self):
        super().__init__()
        self.refresh_config()

    def check_config(self):
        """
        Check if config.ini contains logging settings
        :return: true if configuration contains logging settings
        """
        return super().check_config(section="logging")

    def refresh_config(self):
        """
        Refreshed logging configuration and (re-)-init logging
        """
        super().refresh_config()

        if self.check_config() is not False:
            level = super().read_config("logging", "loglevel")
        else:
            level = "INFO"

        if level is "DEBUG":
            logging.basicConfig(filename='minioclient.log', level=logging.DEBUG)
        if level is "INFO":
            logging.basicConfig(filename='minioclient.log', level=logging.INFO)
        if level is "WARN":
            logging.basicConfig(filename='minioclient.log', level=logging.WARN)
        if level is "ERROR":
            logging.basicConfig(filename='minioclient.log', level=logging.ERROR)
