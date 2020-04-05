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
from datetime import date

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, Slot, QSettings
from PySide2.QtGui import QPixmap, QIcon

# noinspection PyUnresolvedReferences
import resources.all  # noqa: F401
from src.database import get_new_offer_number, get_users_table


class User:
    def __init__(self):
        self.id = None
        self.name = None
        self.phone = None
        self.mail = None
        self.male = True
        self.char_for_offer_symbol = None
        self.business_symbol = None

    @property
    def gender_suffix(self):
        if self.male:
            return ""
        return "a"

    def new_offer_symbol(self):
        """
        Example: I1804P01
            1 char - business symbol,
        2 - 3 char - year,
        4 - 5 char - month,
            6 char - author symbol (M for Mark etc.)
        7 - 8 char - next number for current month for current author
        :return: new offer symbol as string
        """
        year_and_month = date.today().strftime("%y%m")
        number = get_new_offer_number(self.id)
        return f"{self.business_symbol}{year_and_month}{self.char_for_offer_symbol}{number:02}"

    @classmethod
    def from_sql_record(cls, rec):
        user = cls()
        user.id = rec.value("user_id")
        user.name = rec.value("name")
        user.phone = rec.value("phone")
        user.mail = rec.value("mail")
        user.male = rec.value("male")
        user.char_for_offer_symbol = rec.value("char_for_offer_symbol")
        user.business_symbol = rec.value("business_symbol")
        return user


class UserSelectionDialog(QtWidgets.QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.chosen_user_record = None
        self.settings = QSettings()
        default_user = self.settings.value("default_user", 0)

        self.setWindowTitle(self.tr("pyOffer - Choose user"))
        icon = QIcon()
        icon.addFile(u":/ico")
        self.setWindowIcon(icon)

        top_level_layout = QtWidgets.QVBoxLayout(self)
        logo_label = QtWidgets.QLabel(self)
        logo = QPixmap()
        logo.load(u":/klog")
        logo_label.setPixmap(logo)
        logo_label.setAlignment(Qt.AlignCenter)
        top_level_layout.addWidget(logo_label)

        horizontal_layout = QtWidgets.QHBoxLayout()
        icon_label = QtWidgets.QLabel(self)
        pixmap = QPixmap(":/user").scaled(128, 128, Qt.KeepAspectRatio)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        horizontal_layout.addWidget(icon_label)

        vertical_layout = QtWidgets.QVBoxLayout()
        label_description = QtWidgets.QLabel(self)
        label_description.setText(self.tr("Please choose user:"))
        vertical_layout.addWidget(label_description)

        self.list_view = QtWidgets.QListView(self)
        self.list_view.setModel(self.model)
        self.list_view.setModelColumn(1)
        self.list_view.setSelectionBehavior(QtWidgets.QListView.SelectRows)
        self.list_view.setCurrentIndex(self.model.index(default_user, 1))
        vertical_layout.addWidget(self.list_view)

        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.ok)
        self.buttons.rejected.connect(self.reject)
        vertical_layout.addWidget(self.buttons)

        horizontal_layout.addLayout(vertical_layout)
        top_level_layout.addLayout(horizontal_layout)

    @Slot()
    def ok(self) -> None:
        row = self.list_view.currentIndex().row()
        self.chosen_user_record = self.model.record(row)
        self.settings.setValue("default_user", row)
        self.accept()

    @staticmethod
    def make():
        user_model = get_users_table()
        return UserSelectionDialog(user_model)
