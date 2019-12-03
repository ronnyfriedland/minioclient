from config.Configuration import Configuration


class MinioConfiguration(Configuration):
    """
    Author: Ronny Friedland

    Handles minio configuration
    """

    CONFIG_DEFAULTS = {'ssl': 'False', 'debug': 'True'}

    def __init__(self, config_file = Configuration.config_file):
        super().__init__(config_file)

    def check_config(self):
        """
        Check if config.ini contains minio settings
        :return: true if configuration contains minio settings
        """
        return super().check_config(section="minio")

    def write_config(self, url, access_key, secret_key):
        """
        Write new configuration
        :param url: minio url
        :param access_key: minio access key
        :param secret_key: minio secret key
        """
        data = self.CONFIG_DEFAULTS
        data["url"] = url
        data["accesskey"] = access_key
        data["secretkey"] = secret_key
        super().write_config(section="minio", data=data)
        super().refresh_config()

    def read_config(self):
        """
        Reads authentication configuration
        :return: url, access_key, secret_key
        """
        url = super().read_config(section="minio", key="url")
        access_key = super().read_config(section="minio", key="accesskey")
        secret_key = super().read_config(section="minio", key="secretkey")

        return url, access_key, secret_key

    def read_config(self, key):
        """
        Reads authentication configuration key
        :param key: the configuration key
        :return: value of key
        """
        return super().read_config(section="minio", key=key)
