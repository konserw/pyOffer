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

import typing
from enum import Enum, unique

from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, Slot, QObject
from PySide2.QtSql import QSqlRecord
from PySide2.QtWidgets import QDialog

from forms.ui_terms_chooser_dialog import Ui_TermsChooserDialog
from src.database import get_terms_table


@unique
class TermType(Enum):
    delivery = 0
    offer = 1
    billing = 2
    delivery_date = 3
    remarks = 4


class TermItem:
    pl_type_descs = {
        TermType.delivery: "Warunki dostawy",
        TermType.offer: "Warunki oferty",
        TermType.billing: "Warunki plałatności",
        TermType.delivery_date: "Termin dostawy",
        TermType.remarks: "Uwagi"
    }

    def __init__(self, term_type: TermType):
        self.type = term_type
        self.id = None
        self.short_desc = None
        self.long_desc = None
        self.type_description = self.pl_type_descs[term_type]

    @staticmethod
    def from_record(term_type: TermType, record: QSqlRecord) -> TermItem:
        t = TermItem(term_type)
        t.type = term_type
        t.id = record.value("term_id")
        t.short_desc = record.value("short_desc")
        t.long_desc = record.value("long_desc")
        return t


class TermModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.list = []
        self.headers = (
            self.tr("Id"),
            self.tr("Short description"),
            self.tr("Option text"),
        )

    def add(self, item: TermItem) -> None:
        self.list.append(item)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self.list)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return 3

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole and index.isValid() and row < self.rowCount():
            t = self.list[row]
            if column == 0:
                return str(t.id)
            elif column == 1:
                return t.short_desc
            elif column == 2:
                return t.long_desc

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return str(section)
            return self.headers[section]
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        return Qt.NoItemFlags

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if row < len(self.list):
            return super().createIndex(row, column, self.list[row])
        return super().index(row, column, parent)


class TermsChooserDialog(QDialog):
    def __init__(self, term_type, term_model, parent=None):
        super().__init__(parent)
        self.ui = Ui_TermsChooserDialog()
        self.ui.setupUi(self)
        self.term_type = term_type
        self.term_model = term_model
        self.chosen_item = None

        self.titles = {
            TermType.billing: self.tr("Choose billing terms"),
            TermType.delivery: self.tr("Choose delivery terms"),
            TermType.delivery_date: self.tr("Choose delivery date terms"),
            TermType.offer: self.tr("Choose offer terms")
        }
        self.setWindowTitle(self.titles[term_type])

        self.ui.listView.setModel(self.term_model)
        self.ui.listView.setModelColumn(1)
        self.ui.listView.clicked.connect(self.selection_changed)

    @Slot(QModelIndex)
    def selection_changed(self, index: QModelIndex) -> None:
        self.chosen_item = index.internalPointer()
        self.ui.plainTextEdit.setPlainText(self.chosen_item.long_desc)

    @classmethod
    def make(cls, term_type: TermType, parent: QObject = None) -> TermsChooserDialog:
        table = get_terms_table(term_type.value)
        model = TermModel(parent)
        for i in range(table.rowCount()):
            model.add(TermItem.from_record(term_type, table.record(i)))
        return cls(term_type, model, parent)
