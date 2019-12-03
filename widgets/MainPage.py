import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from client.MinioClient import MinioClient
from config.LoggingConfiguration import LoggingConfiguration
from config.MinioConfiguration import MinioConfiguration
from widgets.LoginPage import LoginPage


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

        self._minio = MinioClient(minio_config.read_config("url"), minio_config.read_config("accesskey"), minio_config.read_config("secretkey"))

        self._list_buckets = QComboBox()
        self._list_buckets.activated[str].connect(self.do_refresh_objects)

        self._refresh_buckets = QPushButton("&Refresh")
        self._refresh_buckets.clicked.connect(self.do_refresh_buckets)

        self._list_objects = CustomQTableWidget(self)
        self._list_objects.setSelectionMode(QAbstractItemView.SingleSelection)
        self._list_objects.doubleClicked.connect(self.do_object_selected)
        self._list_objects.setContextMenuPolicy(Qt.CustomContextMenu)
        self._list_objects.customContextMenuRequested.connect(self.do_object_context_selected)

        self._path = QPushButton()
        self._path.clicked.connect(self.do_select_parent_directory)

        self._menu1 = QMenu()
        self._upload_action = self._menu1.addAction("&Upload")
        self._download_action = self._menu1.addAction("&Download")
        self._remove_action = self._menu1.addAction("&Remove")

        self._menu2 = QMenu()
        self._menu2.addAction("&Upload").triggered.connect(self.upload_selected)
        self._menu2.addAction("&Quit").triggered.connect(self.quit_selected)

        self._status = QLabel()
        self._status.setText("Ready")

        layout = QHBoxLayout()
        layout.addWidget(self._list_buckets)
        layout.addWidget(self._refresh_buckets)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addLayout(layout, 1, 0)
        grid.addWidget(self._path, 2, 0)
        grid.addWidget(self._list_objects, 3, 0)
        grid.addWidget(self._status, 4, 0)

        self.setLayout(grid)
        self.setMinimumSize(800, 600)

        #self._setStyleSheet(open('assets/darkstyle.qss').read())
        self.setWindowIcon(QIcon('assets/icon_app.png'))

        self._trayIcon = QSystemTrayIcon(QIcon('assets/icon_app.png'), qApp)
        self._trayIcon.setContextMenu(self._menu2)
        self._trayIcon.show()

        self.show()

        self.do_refresh_buckets()
        self.do_refresh_objects(self._list_buckets.currentText())

    def do_refresh_objects(self, text, directory=''):
        self._path.setText(directory)
        self._list_objects.clear()
        self._list_objects.setRowCount(0)
        self._list_objects.setColumnCount(4)
        self._list_objects.setHorizontalHeaderItem(0, QTableWidgetItem("Directory"))
        self._list_objects.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self._list_objects.setHorizontalHeaderItem(2, QTableWidgetItem("Last Modified"))
        self._list_objects.setHorizontalHeaderItem(3, QTableWidgetItem("Size (Bytes)"))

        header = self._list_objects.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        row=0
        for object in self._minio.list_objects(text, directory):
            self._list_objects.insertRow(row)
            if object.is_dir:
                self._list_objects.setItem(row, 0, QTableWidgetItem(object.object_name))
                self._list_objects.setItem(row, 1, QTableWidgetItem(""))
                self._list_objects.setItem(row, 2, QTableWidgetItem(""))
                self._list_objects.setItem(row, 3, QTableWidgetItem(""))
            else:
                self._list_objects.setItem(row, 0, QTableWidgetItem(""))
                self._list_objects.setItem(row, 1, QTableWidgetItem(object.object_name))
                self._list_objects.setItem(row, 2, QTableWidgetItem(str(object.last_modified)))
                self._list_objects.setItem(row, 3, QTableWidgetItem(str(object.size)))

            row = row + 1

    def do_refresh_buckets(self):
        self._list_buckets.clear()
        buckets = self._minio.list_buckets()
        if buckets is not None:
            for bucket in buckets:
                self._list_buckets.addItem(bucket.name)

    def do_object_selected(self, row):
        if self._list_objects.item(row.row(), 0).text() is "":
            # object
            self.download(self._list_buckets.currentText(), self._list_objects.item(row.row(), 1).text())
        else:
            # directory
            self.do_refresh_objects(self._list_buckets.currentText(), self._list_objects.item(row.row(), 0).text())

    def do_object_context_selected(self, pos):
        action = self._menu1.exec_(self._list_objects.mapToGlobal(pos))
        if action == self._download_action:
            row = self._list_objects.itemAt(pos).row()
            self.download(self._list_buckets.currentText(), self._list_objects.item(row, 1).text())
        if action == self._upload_action:
            self.upload_selected()
        if action == self._remove_action:
            selection = QMessageBox.question(self, 'Confirm selection', "File will be removed immediately",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if selection == QMessageBox.Yes:
                row = self._list_objects.itemAt(pos).row()
                delete_file = self._list_objects.item(row, 1).text()
                self._minio.delete_object(self._list_buckets.currentText(), delete_file)
                logging.info('Removed file %s' % delete_file)
                self.do_refresh_objects(self._list_buckets.currentText())

    def do_select_parent_directory(self):
        parent_path = "/".join(self._path.text()[:-1].split("/")[:-1])
        self.do_refresh_objects(self._list_buckets.currentText(), parent_path)

    def download(self, bucket_name, object_name):
        self._status.setText("Downloading")
        save_as_file = QFileDialog.getSaveFileName(self, "Save File")
        if save_as_file[0] is not '':
            self._minio.get_object(bucket_name, object_name, save_as_file[0])
        self._status.setText("Ready")

    def upload_selected(self):
        upload_file = QFileDialog.getOpenFileName(self, "Open File")
        self.upload(self._list_buckets.currentText(), upload_file[0])

    def upload(self, bucket_name, upload_file):
        self._status.setText("Uploading")
        if upload_file is not '':
            future = self._minio.put_object(bucket_name, QFileInfo(upload_file).fileName(), upload_file)
            future.add_done_callback(self.upload_finshed)
        self._status.setText("Ready")

    def upload_finshed(self, future):
        self.do_refresh_objects(self._list_buckets.currentText())

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
                self.parent().upload(self.parent()._list_buckets.currentText(), upload_url.toLocalFile())
