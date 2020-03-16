import logging
import sys
from datetime import datetime

from PySide2.QtWidgets import QApplication

from src import database
from src.main_window import MainWindow

VERSION = 0.1

if __name__ == '__main__':
    logging.info("koferta version {} started at {}", VERSION, datetime.now())

    app = QApplication(sys.argv)
    database.connect()

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
