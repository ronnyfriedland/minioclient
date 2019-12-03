from config.Configuration import Configuration

import logging


class LoggingConfiguration(Configuration):
    """
    Author: Ronny Friedland

    Handles logging configuration
    """

    CONFIG_DEFAULTS = {'loglevel':'INFO'}

    def __init__(self, config_file = Configuration.config_file):
        super().__init__(config_file)

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

        if level == "DEBUG":
            logging.basicConfig(filename='minioclient.log', level=logging.DEBUG)
        elif level == "INFO":
            logging.basicConfig(filename='minioclient.log', level=logging.INFO)
        elif level == "WARN":
            logging.basicConfig(filename='minioclient.log', level=logging.WARN)
        else:
            logging.basicConfig(filename='minioclient.log', level=logging.ERROR)
