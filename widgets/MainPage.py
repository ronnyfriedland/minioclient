from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from client.Authentication import Authentication
from client.MinioClient import MinioClient
from widgets.LoginPage import LoginPage

class MainPage(QDialog):

    def __init__(self):
        super().__init__()
        auth = Authentication()

        if auth.check_config() is False:
            LoginPage().exec()

        url, access_key, secret_key = auth.auth()
        self.minio = MinioClient(url, access_key, secret_key)

        self.list_buckets = QComboBox()
        self.list_buckets.activated[str].connect(self.do_refresh_objects)

        self.refresh_buckets = QPushButton("&Refresh")
        self.refresh_buckets.clicked.connect(self.do_refresh_buckets)

        self.list_objects = QTableWidget()
        self.list_objects.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_objects.doubleClicked.connect(self.do_object_selected)
        self.list_objects.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_objects.customContextMenuRequested.connect(self.do_object_context_selected)

        self.menu1 = QMenu()
        self.download_action = self.menu1.addAction("&Download")
        self.remove_action = self.menu1.addAction("&Remove")

        self.menu2 = QMenu()
        self.upload_action = self.menu2.addAction("&Upload")
        self.upload_action.triggered.connect(self.upload_selected)
        self.quit_action = self.menu2.addAction("&Quit")
        self.quit_action.triggered.connect(self.quit_selected)


        self.status = QLabel()
        self.status.setText("Ready")

        layout = QHBoxLayout()
        layout.addWidget(self.list_buckets)
        layout.addWidget(self.refresh_buckets)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addLayout(layout, 1, 0)
        grid.addWidget(self.list_objects, 2, 0)
        grid.addWidget(self.status, 3, 0)

        self.setLayout(grid)
        self.setMinimumSize(600, 400)

        self.setStyleSheet(open('assets/darkstyle.qss').read())
        self.setWindowIcon(QIcon('assets/icon_app.png'))

        self.trayIcon = QSystemTrayIcon(QIcon('assets/icon_app.png'), qApp)
        self.trayIcon.setContextMenu(self.menu2)
        self.trayIcon.show()

        self.show()

        self.do_refresh_buckets()
        self.do_refresh_objects(self.list_buckets.currentText())


    def do_refresh_objects(self, text, directory=''):
        self.list_objects.clear()
        self.list_objects.setRowCount(0)
        self.list_objects.setColumnCount(5)
        self.list_objects.setHorizontalHeaderItem(0, QTableWidgetItem("Bucket"))
        self.list_objects.setHorizontalHeaderItem(1, QTableWidgetItem("Directory"))
        self.list_objects.setHorizontalHeaderItem(2, QTableWidgetItem("Name"))
        self.list_objects.setHorizontalHeaderItem(3, QTableWidgetItem("Last Modified"))
        self.list_objects.setHorizontalHeaderItem(4, QTableWidgetItem("Size (Bytes)"))

        header = self.list_objects.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        row=0
        for object in self.minio.list_objects(text, directory):
            self.list_objects.insertRow(row)
            self.list_objects.setItem(row, 0, QTableWidgetItem(object.bucket_name))
            if object.is_dir:
                self.list_objects.setItem(row, 1, QTableWidgetItem(object.object_name))
                self.list_objects.setItem(row, 2, QTableWidgetItem(""))
                self.list_objects.setItem(row, 3, QTableWidgetItem(""))
                self.list_objects.setItem(row, 4, QTableWidgetItem(""))
            else:
                self.list_objects.setItem(row, 1, QTableWidgetItem(""))
                self.list_objects.setItem(row, 2, QTableWidgetItem(object.object_name))
                self.list_objects.setItem(row, 3, QTableWidgetItem(str(object.last_modified)))
                self.list_objects.setItem(row, 4, QTableWidgetItem(str(object.size)))

            row = row + 1

    def do_refresh_buckets(self):
        self.list_buckets.clear()
        buckets = self.minio.list_buckets()
        if buckets is not None:
            for bucket in buckets:
                self.list_buckets.addItem(bucket.name)

    def do_object_selected(self, row):
        if self.list_objects.item(row.row(), 1) is None:
            # object
            self.download(self.list_objects.item(row.row(), 0).text(), self.list_objects.item(row.row(), 2).text())
        else:
            # directory
            self.do_refresh_objects(self.list_buckets.currentText(), self.list_objects.item(row.row(), 1).text())

    def do_object_context_selected(self, pos):
        action = self.menu1.exec_(self.list_objects.mapToGlobal(pos))
        if action == self.download_action:
            row = self.list_objects.itemAt(pos).row()
            self.download(self.list_objects.item(row, 0).text(), self.list_objects.item(row, 2).text())
        if action == self.remove_action:
            selection = QMessageBox.question(self, 'Confirm selection', "File will be removed immediately",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if selection == QMessageBox.Yes:
                row = self.list_objects.itemAt(pos).row()
                self.minio.delete_object(self.list_objects.item(row, 0).text(), self.list_objects.item(row, 2).text())
                self.do_refresh_objects(self.list_buckets.currentText())


    def download(self, bucket_name, object_name):
        self.status.setText("Downloading")
        save_as_file = QFileDialog.getSaveFileName(self, "Save File")
        if save_as_file[0] is not '':
            self.minio.get_object(bucket_name, object_name, save_as_file[0])
            self.status.setText("Ready")

    def upload_selected(self):
        # TODO: implement me
        raise Warning("Not implemented yet")

    def quit_selected(self):
        qApp.quit()