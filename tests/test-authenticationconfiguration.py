import unittest as ut
import os

from config.AuthenticationConfiguration import AuthenticationConfiguration


class TestAuthenticationConfiguration(ut.TestCase):

    def test_init(self):
        result = AuthenticationConfiguration()
        assert result.configuration is not None

    def test_has_section(self):
        assert AuthenticationConfiguration().check_config() == True

    def test_read(self):
        assert AuthenticationConfiguration().read_config() == ("1", "2", "3")

    @classmethod
    def setUpClass(cls):
        test_data = """
        [minio]
        url=1
        accesskey=2
        secretkey=3
        """
        with open('config.ini', "w") as config_file:
            config_file.write(test_data)

    @classmethod
    def tearDownClass(cls):
        os.remove("config.ini")


if __name__ == '__main__':
    ut.main()