import sys
import logging
import pyqt5ac

from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    db = QSqlDatabase.addDatabase("QPSQL")
    db.setHostName("127.0.0.1")
    db.setDatabaseName("koferta_test")
    db.setUserName("postgres")
    db.setPassword("docker")
    ok = db.open()
    if not ok:
        logging.error("Failed to open database")
        logging.error(db.lastError().text())

    pyqt5ac.main(config='pyqt5ac.json')
    from src.main_window import MainWindow
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
