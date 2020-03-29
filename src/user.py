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
from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap, QIcon

# noinspection PyUnresolvedReferences
import resources.all  # noqa: F401
from src.database import get_new_offer_number


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
    def __init__(self, model, default_user=0, parent=None):
        super().__init__(parent)
        self.model = model

        self.setWindowTitle(self.tr("pyOffer - Choose user"))
        icon = QIcon()
        icon.addFile(u":/ico", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(400, 400)
        self.vertical_layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel(self)
        logo = QPixmap()
        logo.load(u":/klog")
        self.label.setPixmap(logo)
        self.vertical_layout.addWidget(self.label)

        self.label2 = QtWidgets.QLabel(self)
        self.label.setText(self.tr("Please choose user:"))
        self.vertical_layout.addWidget(self.label2)

        self.list = QtWidgets.QListView(self)
        self.list.setModel(self.model)
        self.list.setModelColumn(1)
        self.list.setSelectionBehavior(QtWidgets.QListView.SelectRows)
        self.list.setCurrentIndex(self.model.index(default_user, 1))
        self.vertical_layout.addWidget(self.list)

        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.vertical_layout.addWidget(self.buttons)
