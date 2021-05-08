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

import logging

from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QModelIndex, Qt, Slot, QObject
from PySide2.QtSql import QSqlTableModel, QSqlRecord
from PySide2.QtWidgets import QWidget, QDialog, QHeaderView
from src.database import get_company_names_model, get_addresses_model, create_customer


class Customer:
    def __init__(self):
        self.id = None
        self.title = ""
        self.first_name = ""
        self.last_name = ""
        self.company_name = ""
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
        return "{}\n{}\n{}".format(self.concated_name, self.company_name, self.address)

    def __str__(self) -> str:
        return "<Customer {}: {}; {}>".format(self.id, self.concated_name, self.company_name)

    @staticmethod
    def from_record(record: QSqlRecord) -> Customer:
        c = Customer()
        c.id = record.value("customer_id")
        c.title = record.value("title")
        c.first_name = record.value("first_name")
        c.last_name = record.value("last_name")
        c.company_name = record.value("company_name")
        c.address = record.value("address").replace("\\n", "\n")
        return c


class CustomerSearchModel(QSqlTableModel):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.setTable("customers")
        self.select()
        self.headers = (self.tr("Customer name"), self.tr("Company name"), self.tr("Address"))

    def columnCount(self, index: QModelIndex = QModelIndex) -> int:
        return 3

    def data(self, index: QModelIndex, role: int = ...):
        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole and index.isValid() and row < self.rowCount():
            customer = Customer.from_record(self.record(row))
            if column == 0:
                return customer.concated_name
            elif column == 1:
                return customer.company_name
            elif column == 2:
                return customer.address
        return super().data(index, role)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.NoItemFlags

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return str(section)
            return self.headers[section]
        return super().headerData(section, orientation, role)

    @Slot(str)
    def search(self, pattern: str) -> None:
        super().setFilter("first_name ilike '%{0}%' or company_name ilike '%{0}%' or last_name ilike '%{0}%'".format(pattern))


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
        self.resize(1200, 900)
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
        logging.debug("Creating %s", cls.__name__)
        model = CustomerSearchModel(parent)
        return cls(model, parent)


class CreateCustomerDialog(QtWidgets.QDialog):
    def __init__(self, company_names_model, addresses_model, parent: QObject = None):
        super().__init__(parent)
        self.company_names_model = company_names_model
        self.addresses_model = addresses_model

        self.setWindowTitle(self.tr("Create customer"))
        self.resize(620, 480)

        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setSpacing(6)
        self.grid_layout.setContentsMargins(11, 11, 11, 11)
        self.grid_layout.setObjectName("gridLayout")

        label = QtWidgets.QLabel(self)
        label.setText(self.tr("Title:"))
        self.grid_layout.addWidget(label, 0, 0, 1, 1)
        self.line_edit_title = QtWidgets.QLineEdit(self)
        self.grid_layout.addWidget(self.line_edit_title, 0, 1, 1, 1)

        label = QtWidgets.QLabel(self)
        label.setText(self.tr("First name:"))
        self.grid_layout.addWidget(label, 1, 0, 1, 1)
        self.line_edit_first_name = QtWidgets.QLineEdit(self)
        self.grid_layout.addWidget(self.line_edit_first_name, 1, 1, 1, 1)

        label = QtWidgets.QLabel(self)
        label.setText(self.tr("Last name:"))
        self.grid_layout.addWidget(label, 2, 0, 1, 1)
        self.line_edit_last_name = QtWidgets.QLineEdit(self)
        self.grid_layout.addWidget(self.line_edit_last_name, 2, 1, 1, 1)

        label = QtWidgets.QLabel(self)
        label.setText(self.tr("Company name:"))
        self.grid_layout.addWidget(label, 3, 0, 1, 1)
        self.line_edit_company_name = QtWidgets.QLineEdit(self)
        completer = QtWidgets.QCompleter(self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setModel(self.company_names_model)
        self.line_edit_company_name.setCompleter(completer)
        self.grid_layout.addWidget(self.line_edit_company_name, 3, 1, 1, 1)

        label = QtWidgets.QLabel(self)
        label.setText(self.tr("Address:"))
        self.grid_layout.addWidget(label, 4, 0, 1, 1)
        self.line_edit_address = QtWidgets.QLineEdit(self)
        completer = QtWidgets.QCompleter(self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setModel(self.addresses_model)
        self.line_edit_address.setCompleter(completer)
        self.grid_layout.addWidget(self.line_edit_address, 4, 1, 1, 1)

        vertical_spacer = QtWidgets.QSpacerItem(20, 135, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.grid_layout.addItem(vertical_spacer, 5, 0, 1, 2)

        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.Reset)
        self.button_box.accepted.connect(self.save)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.reset)
        self.grid_layout.addWidget(self.button_box, 6, 0, 1, 2)

    @classmethod
    def make(cls, parent: QObject = None) -> CreateCustomerDialog:
        logging.debug("Creating %s", cls.__name__)
        names_model = get_company_names_model()
        addresses_model = get_addresses_model()
        return cls(names_model, addresses_model, parent)

    @Slot()
    def save(self) -> None:
        try:
            create_customer(
                self.line_edit_title.text(),
                self.line_edit_first_name.text(),
                self.line_edit_last_name.text(),
                self.line_edit_company_name.text(),
                self.line_edit_address.text()
            )
        except RuntimeError as e:
            QtWidgets.QMessageBox.warning(self, self.tr("Database operation failed"), str(e))
        else:
            QtWidgets.QMessageBox.information(self, self.tr("Success"), self.tr(f"Created new customer."))

    @Slot()
    def reset(self) -> None:
        self.line_edit_title.clear()
        self.line_edit_first_name.clear()
        self.line_edit_last_name.clear()
        self.line_edit_company_name.clear()
        self.line_edit_address.clear()
