from PyQt5 import QtWidgets
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from client.MinioClient import MinioClient
from config.MinioConfiguration import MinioConfiguration
from config.LoggingConfiguration import LoggingConfiguration
from widgets.LoginPage import LoginPage

import logging, time

class MainPage(QDialog):

    """
    Author: Ronny Friedland

    Main dialog
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # init config
        LoggingConfiguration()
        minio_config = MinioConfiguration()

        if minio_config.check_config() is False:
            LoginPage().exec()

        url, access_key, secret_key = minio_config.read_config()
        self.minio = MinioClient(url, access_key, secret_key)

        self.list_buckets = QComboBox()
        self.list_buckets.activated[str].connect(self.do_refresh_objects)

        self.refresh_buckets = QPushButton("&Refresh")
        self.refresh_buckets.clicked.connect(self.do_refresh_buckets)

        self.list_objects = CustomQTableWidget(self)
        self.list_objects.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_objects.doubleClicked.connect(self.do_object_selected)
        self.list_objects.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_objects.customContextMenuRequested.connect(self.do_object_context_selected)

        self.path = QPushButton()
        self.path.clicked.connect(self.do_select_parent_directory)

        self.menu1 = QMenu()
        self.upload_action = self.menu1.addAction("&Upload")
        self.download_action = self.menu1.addAction("&Download")
        self.remove_action = self.menu1.addAction("&Remove")

        self.menu2 = QMenu()
        self.menu2.addAction("&Upload").triggered.connect(self.upload_selected)
        self.menu2.addAction("&Quit").triggered.connect(self.quit_selected)

        self.status = QLabel()
        self.status.setText("Ready")

        layout = QHBoxLayout()
        layout.addWidget(self.list_buckets)
        layout.addWidget(self.refresh_buckets)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addLayout(layout, 1, 0)
        grid.addWidget(self.path, 2, 0)
        grid.addWidget(self.list_objects, 3, 0)
        grid.addWidget(self.status, 4, 0)

        self.setLayout(grid)
        self.setMinimumSize(800, 600)

        #self.setStyleSheet(open('assets/darkstyle.qss').read())
        self.setWindowIcon(QIcon('assets/icon_app.png'))

        self.trayIcon = QSystemTrayIcon(QIcon('assets/icon_app.png'), qApp)
        self.trayIcon.setContextMenu(self.menu2)
        self.trayIcon.show()

        self.show()

        self.do_refresh_buckets()
        self.do_refresh_objects(self.list_buckets.currentText())

    def do_refresh_objects(self, text, directory=''):
        self.path.setText(directory)
        self.list_objects.clear()
        self.list_objects.setRowCount(0)
        self.list_objects.setColumnCount(4)
        self.list_objects.setHorizontalHeaderItem(0, QTableWidgetItem("Directory"))
        self.list_objects.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.list_objects.setHorizontalHeaderItem(2, QTableWidgetItem("Last Modified"))
        self.list_objects.setHorizontalHeaderItem(3, QTableWidgetItem("Size (Bytes)"))

        header = self.list_objects.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        row=0
        for object in self.minio.list_objects(text, directory):
            self.list_objects.insertRow(row)
            if object.is_dir:
                self.list_objects.setItem(row, 0, QTableWidgetItem(object.object_name))
                self.list_objects.setItem(row, 1, QTableWidgetItem(""))
                self.list_objects.setItem(row, 2, QTableWidgetItem(""))
                self.list_objects.setItem(row, 3, QTableWidgetItem(""))
            else:
                self.list_objects.setItem(row, 0, QTableWidgetItem(""))
                self.list_objects.setItem(row, 1, QTableWidgetItem(object.object_name))
                self.list_objects.setItem(row, 2, QTableWidgetItem(str(object.last_modified)))
                self.list_objects.setItem(row, 3, QTableWidgetItem(str(object.size)))

            row = row + 1

    def do_refresh_buckets(self):
        self.list_buckets.clear()
        buckets = self.minio.list_buckets()
        if buckets is not None:
            for bucket in buckets:
                self.list_buckets.addItem(bucket.name)

    def do_object_selected(self, row):
        if self.list_objects.item(row.row(), 0).text() is "":
            # object
            self.download(self.list_buckets.currentText(), self.list_objects.item(row.row(), 1).text())
        else:
            # directory
            self.do_refresh_objects(self.list_buckets.currentText(), self.list_objects.item(row.row(), 0).text())

    def do_object_context_selected(self, pos):
        action = self.menu1.exec_(self.list_objects.mapToGlobal(pos))
        if action == self.download_action:
            row = self.list_objects.itemAt(pos).row()
            self.download(self.list_buckets.currentText(), self.list_objects.item(row, 1).text())
        if action == self.upload_action:
            self.upload_selected()
        if action == self.remove_action:
            selection = QMessageBox.question(self, 'Confirm selection', "File will be removed immediately",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if selection == QMessageBox.Yes:
                row = self.list_objects.itemAt(pos).row()
                delete_file = self.list_objects.item(row, 1).text()
                self.minio.delete_object(self.list_buckets.currentText(), delete_file)
                logging.info('Removed file %s' % delete_file)
                self.do_refresh_objects(self.list_buckets.currentText())

    def do_select_parent_directory(self):
        parent_path = "/".join(self.path.text()[:-1].split("/")[:-1])
        self.do_refresh_objects(self.list_buckets.currentText(), parent_path)

    def download(self, bucket_name, object_name):
        self.status.setText("Downloading")
        save_as_file = QFileDialog.getSaveFileName(self, "Save File")
        if save_as_file[0] is not '':
            self.minio.get_object(bucket_name, object_name, save_as_file[0])
        self.status.setText("Ready")

    def upload_selected(self):
        upload_file = QFileDialog.getOpenFileName(self, "Open File")
        self.upload(self.list_buckets.currentText(), upload_file[0])

    def upload(self, bucket_name, upload_file):
        self.status.setText("Uploading")
        if upload_file is not '':
            future = self.minio.put_object(bucket_name, QFileInfo(upload_file).fileName(), upload_file)
            future.add_done_callback(self.upload_finshed)
        self.status.setText("Ready")

    def upload_finshed(self, future):
        self.do_refresh_objects(self.list_buckets.currentText())

    def quit_selected(self):
        qApp.quit()


class CustomQTableWidget(QTableWidget):

    """
    Author: Ronny Friedland

    Custom QTableWidget to provide drag'n'drop for file upload
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        selection = QMessageBox.question(self, 'Confirm selection', "File will be uploaded immediately",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if selection == QMessageBox.Yes:
            for upload_url in e.mimeData().urls():
                self.parent().upload(self.parent().list_buckets.currentText(), upload_url.toLocalFile())
