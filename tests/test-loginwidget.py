import sys
import unittest as ut
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
from unittest.mock import MagicMock, patch

from config.MinioConfiguration import MinioConfiguration
from widgets.LoginPage import LoginPage


class TestLoginWidget(ut.TestCase):

    app = QApplication(sys.argv)

    def test_init(self):
        subject = LoginPage()
        self.assertEqual(subject._url.text(), "")
        self.assertEqual(subject._access_key.text(), "")
        self.assertEqual(subject._secret_key.text(), "")
        self.assertEqual(subject._secret_key.echoMode(), QLineEdit.Password)

    @patch.object(QDialog, 'close')
    @patch.object(MinioConfiguration, 'write_config', MagicMock())
    def test_save(self, mock):
        subject = LoginPage()
        subject.save_config()
        self.assertTrue(mock.called)


if __name__ == '__main__':
    ut.main()
