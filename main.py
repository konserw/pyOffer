import sys
import logging
from datetime import datetime
import pyqt5ac

from PyQt5.QtWidgets import QApplication

VERSION = 0.1

if __name__ == '__main__':
    logging.info("koferta version {} started at {}", VERSION, datetime.now())
    app = QApplication(sys.argv)

    pyqt5ac.main(config='pyqt5ac.json')
    from src.main_window import MainWindow
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
