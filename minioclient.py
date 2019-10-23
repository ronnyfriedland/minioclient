import sys

from PyQt5.QtWidgets import *

from widgets.MainPage import MainPage

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainPage()
    sys.exit(app.exec_())
