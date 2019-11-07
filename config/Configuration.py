from configparser import ConfigParser

CONFIG_FILE = 'config.ini'


class Configuration:
    """
    Author: Ronny Friedland

    Handles common configuration access
    """

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(CONFIG_FILE)

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

        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def read_config(self, section, key):
        """
        Reads the configutation value for the given key
        :param section: the section to read
        :param key: the key to evaluate
        :return: the stored value for the given key
        """
        #if not self.check_config(section):
        #    return None

        return self.config.get(section, key)
