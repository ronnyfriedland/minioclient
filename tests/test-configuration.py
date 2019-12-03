import unittest as ut
import os

from config.Configuration import Configuration


class TestConfiguration(ut.TestCase):

    def test_init(self):
        result = Configuration("config-test.ini")
        self.assertIsNotNone(result.config)

    def test_has_section(self):
        self.assertFalse(Configuration("config-test.ini").check_config("test-unknown"))
        self.assertTrue(Configuration("config-test.ini").check_config("test"))

    def test_read(self):
        self.assertEqual(Configuration("config-test.ini").read_config("test", "foo"), "bar")

    def test_write(self):
        Configuration("config-test.ini").write_config("test", {"foo": "bar"})

        self.assertTrue(Configuration("config-test.ini").check_config("test"))
        self.assertEqual(Configuration("config-test.ini").read_config("test", "foo"), "bar")

    @classmethod
    def setUpClass(cls):
        test_data = """
        [test]
        foo=bar
        """
        with open('config-test.ini', "w") as config_file:
            config_file.write(test_data)

    @classmethod
    def tearDownClass(cls):
        os.remove("config-test.ini")


if __name__ == '__main__':
    ut.main()