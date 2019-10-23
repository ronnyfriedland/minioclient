from config.Configuration import Configuration


class Authentication:

    def __init__(self):
        self.configuration = Configuration()

    def check_config(self):
        return self.configuration.check_config("minio")

    def write_config(self, url, access_key, secret_key):
        self.configuration.write_config("minio", {'url': url,
                                                   'accesskey': access_key,
                                                   'secretkey': secret_key})

    def auth(self):
        url = self.configuration.read_config("minio", "url")
        access_key = self.configuration.read_config("minio", "accesskey")
        secret_key = self.configuration.read_config("minio", "secretkey")

        return url, access_key, secret_key
