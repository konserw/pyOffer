# pyOffer - program for creating business proposals for purchase of items
# Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
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
