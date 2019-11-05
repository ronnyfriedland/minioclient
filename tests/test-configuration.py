import unittest as ut
import os

from config.Configuration import Configuration


class TestConfiguration(ut.TestCase):

    def test_init(self):
        result = Configuration()
        assert result.config is not None

    def test_has_section(self):
        assert Configuration().check_config("test-unknown") == False
        assert Configuration().check_config("test") == True

    def test_read(self):
        assert Configuration().read_config("test", "foo") == "bar"

    def test_write(self):
        Configuration().write_config("test", {"foo": "bar"})

        assert Configuration().check_config("test") is True
        assert Configuration().read_config("test", "foo") == "bar"

    @classmethod
    def setUpClass(cls):
        test_data = """
        [test]
        foo=bar
        """
        with open('config.ini', "w") as config_file:
            config_file.write(test_data)

    @classmethod
    def tearDownClass(cls):
        os.remove("config.ini")


if __name__ == '__main__':
    ut.main()