from config.Configuration import Configuration


class AuthenticationConfiguration:

    """
    Author: Ronny Friedland

    Handles minio authentication configuration
    """

    def __init__(self):
        self.configuration = Configuration()

    def check_config(self):
        """
        Check if config.ini contains minio settings
        :return: true if configuration contains minio settings
        """
        return self.configuration.check_config("minio")

    def write_config(self, url, access_key, secret_key):
        """
        Write new configuration
        :param url: minio url
        :param access_key: minio access key
        :param secret_key: minio secret key
        """
        self.configuration.write_config("minio", {'url': url,
                                                   'accesskey': access_key,
                                                   'secretkey': secret_key})

    def read_config(self):
        """
        Reads authentication configuration
        :return: url, access_key, secret_key
        """
        url = self.configuration.read_config("minio", "url")
        access_key = self.configuration.read_config("minio", "accesskey")
        secret_key = self.configuration.read_config("minio", "secretkey")

        return url, access_key, secret_key
