from PyQt5.QtWidgets import *
from client.Authentication import Authentication


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

        url = QLineEdit()
        access_key = QLineEdit()
        secret_key = QLineEdit()

        layout1 = QGridLayout()
        layout1.addWidget(QLabel('URL'), 0, 0)
        layout1.addWidget(url, 0, 1)
        layout1.addWidget(QLabel('Access Key'), 1, 0)
        layout1.addWidget(access_key, 1, 1)
        layout1.addWidget(QLabel('Secret Key'), 2, 0)
        layout1.addWidget(secret_key, 2, 1)

        login_button = QPushButton("&Login")
        login_button.clicked.connect(self.save_config)

        layout1.addWidget(login_button)
        self.setLayout(layout1)
        self.setWindowTitle("Configure Minio access")

    def save_config(self):
        """
        Writes the provided login parameters to configuration.
        """
        auth = Authentication()
        auth.write_config(self.url.text(), self.access_key.text(), self.secret_key.text())
        self.close()
