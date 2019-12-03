from PyQt5.QtWidgets import *
from config.MinioConfiguration import MinioConfiguration
import logging


class LoginPage(QDialog):

    """
    A class used provide a login dialog to sign in to S3 storage

    Methods
    -------
    save_config()
        Writes the input parameters to config file which is used for login
    """

    def __init__(self):
        super().__init__()

        self._url = QLineEdit()
        self._access_key = QLineEdit()
        self._secret_key = QLineEdit()
        self._secret_key.setEchoMode(QLineEdit.Password)

        layout = QGridLayout()
        layout.addWidget(QLabel('URL'), 0, 0)
        layout.addWidget(self._url, 0, 1)
        layout.addWidget(QLabel('Access Key'), 1, 0)
        layout.addWidget(self._access_key, 1, 1)
        layout.addWidget(QLabel('Secret Key'), 2, 0)
        layout.addWidget(self._secret_key, 2, 1)

        login_button = QPushButton("&Login")
        login_button.clicked.connect(self.save_config)

        layout.addWidget(login_button)
        self.setLayout(layout)
        self.setWindowTitle("Configure Minio access")

    def save_config(self):
        """
        Writes the provided login parameters to configuration.
        """
        minio_config = MinioConfiguration()
        minio_config.write_config(self._url.text(), self._access_key.text(), self._secret_key.text())

        logging.info('Configuration created ...')

        self.close()

    @property
    def access_key(self):
        return self._access_key
