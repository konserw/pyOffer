# pyOffer - program for creating business proposals for purchase of items
# Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

from PySide2 import QtWidgets
from PySide2.QtCore import QModelIndex, Qt, Slot, QObject
from PySide2.QtSql import QSqlTableModel, QSqlRecord
from PySide2.QtWidgets import QWidget, QDialog, QHeaderView


class Customer:
    def __init__(self):
        self.id = None
        self.short_name = ""
        self.full_name = ""
        self.title = ""
        self.first_name = ""
        self.last_name = ""
        self.address = ""

    @property
    def concated_name(self) -> str:
        return "{} {} {}".format(self.title, self.first_name, self.last_name)

    @property
    def is_valid(self) -> bool:
        return self.id is not None

    @property
    def html_address(self) -> str:
        return self.address.replace("\n", "<br />\n")

    @property
    def db_id(self) -> str:
        return "NULL" if self.id is None else str(self.id)

    @property
    def description(self) -> str:
        return "{}\n{}\n{}".format(self.concated_name, self.full_name, self.address)

    def __str__(self) -> str:
        return "Customer {}: {}; {}".format(self.id, self.concated_name, self.short_name)

    @staticmethod
    def from_record(record: QSqlRecord) -> Customer:
        c = Customer()
        c.id = record.value("customer_id")
        c.short_name = record.value("short_name")
        c.full_name = record.value("full_name")
        c.title = record.value("title")
        c.first_name = record.value("first_name")
        c.last_name = record.value("last_name")
        c.address = record.value("address").replace("\\n", "\n")
        return c


class CustomerSearchModel(QSqlTableModel):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.setTable("customers_view")
        self.select()
        self.headers = (self.tr("Customer name"), self.tr("Company name"))

    def columnCount(self, index: QModelIndex = QModelIndex) -> int:
        return 2

    def data(self, index: QModelIndex, role: int = ...):
        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole and index.isValid() and row < self.rowCount():
            customer = Customer.from_record(self.record(row))
            if column == 0:
                return customer.concated_name
        return super().data(index, role)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return str(section)
            return self.headers[section]
        return super().headerData(section, orientation, role)

    @Slot(str)
    def search(self, pattern: str) -> None:
        super().setFilter("first_name ilike '%{0}%' or full_name ilike '%{0}%' or last_name ilike '%{0}%'".format(pattern))


class CustomerSearchWidget(QWidget):
    def __init__(self, model, parent: QObject = None):
        super().__init__(parent)
        self.model = model
        self.chosen_customer = None

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.line_edit = QtWidgets.QLineEdit(self)
        self.line_edit.textChanged.connect(self.model.search)
        self.verticalLayout.addWidget(self.line_edit)
        self.table_widget = QtWidgets.QTableView(self)
        self.table_widget.clicked.connect(self.selection_changed)
        self.table_widget.setModel(self.model)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.verticalLayout.addWidget(self.table_widget)

    @Slot(QModelIndex)
    def selection_changed(self, index: QModelIndex) -> None:
        self.chosen_customer = Customer.from_record(self.model.record(index.row())) if index.isValid() else None


class CustomerSelectionDialog(QDialog):
    def __init__(self, model, parent: QObject = None):
        super().__init__(parent)
        self.customer_search = CustomerSearchWidget(model)

        self.setWindowTitle(self.tr("Select customer"))
        self.resize(600, 900)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.customer_search)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.push_button_exit = QtWidgets.QPushButton(self)
        self.push_button_exit.setText(self.tr("OK"))
        self.push_button_exit.clicked.connect(self.accept)
        self.horizontalLayout.addWidget(self.push_button_exit)

        self.verticalLayout.addLayout(self.horizontalLayout)

    @property
    def chosen_customer(self) -> Customer:
        return self.customer_search.chosen_customer

    @classmethod
    def make(cls, parent: QObject = None) -> CustomerSelectionDialog:
        model = CustomerSearchModel(parent)
        return cls(model, parent)
