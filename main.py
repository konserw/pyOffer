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

VERSION = 0.4

if __name__ == '__main__':
    if getattr(sys, "frozen", False):
        logging.basicConfig(
            level=logging.INFO,
            filename="pyoffer.log",
            format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
        )

    logging.info("pyOffer version %s started at %s", VERSION, datetime.now())

    app = QApplication(sys.argv)
    app.setOrganizationName("KonserwSoft")
    app.setApplicationName("pyOffer")

    translator = QTranslator()
    lang = QLocale.system().name()[0:2]
    logging.info("Loading translation for: %s", lang)
    translation_file = f"translations/{lang}"
    if translator.load(translation_file):
        app.installTranslator(translator)
        logging.info("Loaded translation: %s", translation_file)
    else:
        logging.warning("Failed to load translation: %s", translation_file)

    settings = QSettings()
    settings.beginGroup("database")
    host_name = settings.value("host_name", "127.0.0.1")
    port = int(settings.value("port", "5432"))
    database_name = settings.value("database_name", "koferta_test")
    user_name = settings.value("user_name", "postgres")
    password = settings.value("password", "docker")
    settings.endGroup()

    try:
        logging.info("DB host name: %s", host_name)
        logging.info("DB port: %s", port)
        logging.info("DB database name: %s", database_name)
        logging.info("DB user name: %s", user_name)
        database.connect(host_name, database_name, user_name, password, port)
    except RuntimeError as e:
        QMessageBox.critical(None, app.tr("Database connection failed"), app.tr(f"Driver error: {e.args[1]}\nDatabase error: {e.args[2]}"))
        sys.exit(str(e))

    user_dialog = UserSelectionDialog.make()
    if user_dialog.exec_() == QDialog.Accepted:
        logging.debug("User dialog accepted")
        user = User.from_sql_record(user_dialog.chosen_user_record)
        logging.info("Chosen user: %s", user)
        main_window = MainWindow(user)
        main_window.show()
        sys.exit(app.exec_())

    logging.info("User hasn't been chosen - exiting")
    sys.exit(0)
