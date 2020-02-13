import sys
import logging
import pyqt5ac

from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QApplication

from src.main_window import MainWindow


if __name__ == '__main__':
    db = QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName("127.0.0.1")
    db.setDatabaseName("flightdb")
    db.setUserName("acarlson")
    db.setPassword("1uTbSbAs")
    ok = db.open()
    if not ok:
        logging.error("Failed to open database")
        logging.error(db.lastError().text())
    pyqt5ac.main(config='pyqt5ac.json')
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
