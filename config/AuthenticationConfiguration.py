from config import Configuration


class AuthenticationConfiguration(Configuration.Configuration):
    """
    Author: Ronny Friedland

    Handles minio authentication configuration
    """

    def __init__(self):
        super().__init__()

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
        super().write_config(section="minio", data={'url': url,
                                                    'accesskey': access_key,
                                                    'secretkey': secret_key,
                                                    'ssl': 'False',
                                                    'debug': 'False'})

    def read_config(self):
        """
        Reads authentication configuration
        :return: url, access_key, secret_key
        """
        url = super().read_config(section="minio", key="url")
        access_key = super().read_config(section="minio", key="accesskey")
        secret_key = super().read_config(section="minio", key="secretkey")

        return url, access_key, secret_key
