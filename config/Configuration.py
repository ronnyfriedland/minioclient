from configparser import ConfigParser


class Configuration:
    """
    Author: Ronny Friedland

    Handles common configuration access
    """

    config_file = 'config.ini'

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = ConfigParser()
        self.refresh_config()

    def check_config(self, section):
        """
        Check if config.ini contains given section
        :param section: section to check
        :return: true if configuration contains section
        """
        return self.config.has_section(section)

    def write_config(self, section, data=None):
        """
        Writes configuration data to section
        :param section: the section to write
        :param data: the configuration data
        """
        if data is None:
            data = dict()
        self.config[section] = data

        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def read_config(self, section, key):
        """
        Reads the configuration value for the given key
        :param section: the section to read
        :param key: the key to evaluate
        :return: the stored value for the given key
        """
        return self.config.get(section, key)

    def refresh_config(self):
        """
        Refreshes the configuration
        """
        self.config.read(self.config_file)

