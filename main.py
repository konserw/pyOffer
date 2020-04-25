# pyOffer - program for creating business proposals for purchase of items
# Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

import logging
import sys
from datetime import datetime

from PySide2.QtCore import QSettings, QTranslator, QLocale
from PySide2.QtWidgets import QApplication, QDialog, QMessageBox

from src import database
from src.main_window import MainWindow
from src.user import User, UserSelectionDialog

VERSION = 0.1

if __name__ == '__main__':
    logging.info("pyOffer version {} started at {}", VERSION, datetime.now())

    app = QApplication(sys.argv)
    app.setOrganizationName("KonserwSoft")
    app.setApplicationName("pyOffer")

    translator = QTranslator()
    translation_file = f"translations/{QLocale.system().name()[0 - 2]}"
    if translator.load(translation_file):
        app.installTranslator(translator)
    else:
        logging.warning(f"Failed to load translation: {translation_file}")

    settings = QSettings()
    settings.beginGroup("database")
    host_name = settings.value("host_name", "127.0.0.1")
    database_name = settings.value("database_name", "koferta_test")
    user_name = settings.value("user_name", "postgres")
    password = settings.value("password", "docker")
    port = int(settings.value("port", "5432"))
    settings.endGroup()

    try:
        database.connect(host_name, database_name, user_name, password, port)
    except RuntimeError as e:
        QMessageBox.critical(None, app.tr("Database connection failed"), app.tr(f"Driver error: {e.args[1]}\nDatabase error: {e.args[2]}"))
        sys.exit(str(e))

    user_dialog = UserSelectionDialog.make()
    if user_dialog.exec_() == QDialog.Accepted:
        user = User.from_sql_record(user_dialog.chosen_user_record)
        main_window = MainWindow(user)
        main_window.show()
        sys.exit(app.exec_())

    sys.exit(0)
