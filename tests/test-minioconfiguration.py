import unittest as ut
import os

from config.MinioConfiguration import MinioConfiguration


class TestAuthenticationConfiguration(ut.TestCase):

    def test_init(self):
        result = MinioConfiguration("config-test.ini")
        self.assertIsNotNone(result.config)

    def test_has_section(self):
        self.assertTrue(MinioConfiguration("config-test.ini").check_config())

    def test_read(self):
        self.assertEqual(MinioConfiguration("config-test.ini").read_config("url"), "1")

    @classmethod
    def setUpClass(cls):
        test_data = """
        [minio]
        url=1
        accesskey=2
        secretkey=3
        """
        with open("config-test.ini", "w") as config_file:
            config_file.write(test_data)

    @classmethod
    def tearDownClass(cls):
        os.remove("config-test.ini")


if __name__ == '__main__':
    ut.main()