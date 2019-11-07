from PyQt5.QtWidgets import *
from config.AuthenticationConfiguration import AuthenticationConfiguration


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

        self.url = QLineEdit()
        self.access_key = QLineEdit()
        self.secret_key = QLineEdit()
        self.secret_key.setEchoMode(QLineEdit.Password)

        layout1 = QGridLayout()
        layout1.addWidget(QLabel('URL'), 0, 0)
        layout1.addWidget(self.url, 0, 1)
        layout1.addWidget(QLabel('Access Key'), 1, 0)
        layout1.addWidget(self.access_key, 1, 1)
        layout1.addWidget(QLabel('Secret Key'), 2, 0)
        layout1.addWidget(self.secret_key, 2, 1)

        login_button = QPushButton("&Login")
        login_button.clicked.connect(self.save_config)

        layout1.addWidget(login_button)
        self.setLayout(layout1)
        self.setWindowTitle("Configure Minio access")

    def save_config(self):
        """
        Writes the provided login parameters to configuration.
        """
        auth = AuthenticationConfiguration()
        auth.write_config(self.url.text(), self.access_key.text(), self.secret_key.text())
        self.close()
