from configparser import ConfigParser

CONFIG_FILE = 'config.ini'


class Configuration:

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(CONFIG_FILE)

    def check_config(self, section):
        return self.config.has_section(section)

    def write_config(self, section, data=None):
        if data is None:
            data = dict()
        self.config[section] = data

        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def read_config(self, section, key):
        if not self.check_config(section):
            return None

        return self.config.get('minio', key)
