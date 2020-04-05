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

from PySide2.QtWidgets import QApplication, QDialog

from src import database
from src.main_window import MainWindow
from src.user import User, UserSelectionDialog

VERSION = 0.1

if __name__ == '__main__':
    logging.info("pyOffer version {} started at {}", VERSION, datetime.now())

    app = QApplication(sys.argv)
    app.setOrganizationName("KonserwSoft")
    app.setApplicationName("pyOffer")

    database.connect()
    user_dialog = UserSelectionDialog.make()
    if user_dialog.exec_() == QDialog.Accepted:
        user = User.from_sql_record(user_dialog.chosen_user_record)
        main_window = MainWindow(user)
        main_window.show()
        sys.exit(app.exec_())

    sys.exit(0)
