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
import typing
from decimal import Decimal

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import QObject, QAbstractTableModel, QModelIndex, Qt, Slot, Signal
from PySide2.QtGui import QIcon, QPixmap, QColor
from PySide2.QtSql import QSqlRecord
from PySide2.QtWidgets import QWidget, QTableView, QItemDelegate, QStyleOptionViewItem

# noinspection PyUnresolvedReferences
import resources.all  # noqa: F401
from src.database import get_merchandise_sql_model, create_merchandise, get_discount_groups_model


class Merchandise:
    def __init__(self, merchandise_id: int = None):
        self.id = merchandise_id
        self.code = None
        self.description = None
        self._list_price = None
        self._discount = Decimal(0)
        self._count = Decimal(0)
        self.by_meter = False  # by default by piece
        self.discount_group = None

    @property
    def list_price(self) -> Decimal:
        return self._list_price

    @list_price.setter
    def list_price(self, value):
        self._list_price = Decimal(value).quantize(Decimal(".01"))

    @property
    def discount(self) -> Decimal:
        return self._discount

    @discount.setter
    def discount(self, value):
        self._discount = Decimal(value).quantize(Decimal("0.1"))

    @property
    def count(self) -> Decimal:
        return self._count

    @count.setter
    def count(self, value):
        self._count = Decimal(value).quantize(Decimal("1"))

    @property
    def unit(self) -> str:
        if self.by_meter:
            return "m.b."
        else:
            return "szt."

    @property
    def price(self) -> Decimal:
        return round(self.list_price * (100 - self.discount) / 100, 2)

    @property
    def total(self) -> Decimal:
        return round(self.price * self.count, 2)

    @staticmethod
    def from_sql_record(record: QSqlRecord) -> Merchandise:
        item = Merchandise()
        item.id = record.value("merchandise_id")
        item.code = record.value("code")
        item.description = record.value("description")
        item.list_price = record.value("list_price")
        item.by_meter = record.value("unit") == "m"
        item.discount_group = record.value("discount_group")
        return item

    def __eq__(self, other) -> bool:
        if isinstance(other, Merchandise):
            return self.id == other.id
        return False

    def __getitem__(self, col: int):
        if col == 0:
            return self.code
        elif col == 1:
            return self.description
        elif col == 2:
            return self.list_price
        elif col == 3:
            return self.discount
        elif col == 4:
            return self.price
        elif col == 5:
            return self.count
        elif col == 6:
            return self.unit
        elif col == 7:
            return self.total
        else:
            raise IndexError()

    def __setitem__(self, key: int, value: float) -> None:
        if key == 3:
            self.discount = value
        elif key == 5:
            self.count = value
        else:
            raise RuntimeError("unexpected assignment")

    def formatted_field(self, col) -> str:
        if col == 0:
            return self.code
        elif col == 1:
            return self.description
        elif col == 2:
            return f"{self.list_price:.20n}"
        elif col == 3:
            return f"{self.discount:.5n}%"
        elif col == 4:
            return f"{self.price:.20n}"
        elif col == 5:
            return f"{self.count}"
        elif col == 6:
            return self.unit
        elif col == 7:
            return f"{self.total:.20n}"
        else:
            raise IndexError()


class MerchandiseListModel(QAbstractTableModel):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.list = []
        self.ex = None
        self.headers = (
            self.tr("Code"),
            self.tr("Description"),
            self.tr("List Price"),
            self.tr("Discount"),
            self.tr("Price"),
            self.tr("Count"),
            self.tr("Unit"),
            self.tr("Total")
        )

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self.list) + 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self.headers)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            if section < len(self.list):
                return str(section + 1)
            return ""
        elif orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self.headers):
            return self.headers[section]

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        row = index.row()
        col = index.column()
        if index.isValid() and role == Qt.EditRole and row < len(self.list) and col in (3, 5):
            self.list[row][col] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if role == Qt.UserRole:
            return self.list[row].id

        if role == Qt.TextAlignmentRole:
            if col > 1:
                return Qt.AlignRight
            return Qt.AlignLeft

        if role == Qt.BackgroundRole and self.ex is not None and row < len(self.list):
            if self.ex.casefold() in self.list[row].code.casefold() or (self.ex and self.ex == self.list[row].discount_group):
                return QColor(0xFC, 0xF7, 0xBB)

        if role == Qt.EditRole and row < len(self.list) and col in (3, 5):
            return self.list[row][col]

        if role == Qt.DisplayRole:
            if row == len(self.list):
                if col == 6:
                    return self.tr("Total:")
                elif col == 7:
                    return f"{self.grand_total:.20n}"
            elif row < len(self.list):
                return self.list[row].formatted_field(col)

    @property
    def grand_total(self) -> Decimal:
        total = Decimal("0.00")
        for item in self.list:
            total += item.total
        return total

    def supportedDropActions(self) -> Qt.DropActions:
        return Qt.MoveAction

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags

        default = Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        row = index.row()
        col = index.column()
        if row == len(self.list):
            return Qt.ItemIsEnabled | Qt.ItemIsDropEnabled

        if col == 3 or col == 5:
            return Qt.ItemIsEditable | default
        return default

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if row > len(self.list):
            return QModelIndex()
        elif row == len(self.list):
            return self.createIndex(row, column, None)
        return self.createIndex(row, column, self.list[row])

    def clear(self) -> None:
        if not self.list:
            return

        self.beginRemoveRows(QModelIndex(), 0, len(self.list))
        self.list.clear()
        self.endRemoveRows()

    def change_item_count(self, item: Merchandise) -> None:
        try:
            idx = self.list.index(item)
        except ValueError:  # item not on the list
            self.add_item(item)
        else:
            self.list[idx].count += item.count

    def removeRows(self, row: int, count: int, parent: QModelIndex = QModelIndex()) -> bool:
        end = row + count - 1
        if end >= len(self.list):
            return False

        self.beginRemoveRows(QModelIndex(), row, end)
        for i in range(row, end + 1):
            self.list.pop(i)
        self.endRemoveRows()
        return True

    def moveRows(self, sourceParent: QModelIndex, sourceRow: int, count: int, destinationParent: QModelIndex, destinationChild: int) -> bool:
        last_row = sourceRow + count - 1
        offset = destinationChild - sourceRow
        if destinationChild == len(self.list):
            offset -= 1

        if self.beginMoveRows(sourceParent, sourceRow, last_row, destinationParent, destinationChild):
            for i in range(count):
                self.list.insert(sourceRow + offset + i, self.list.pop(sourceRow + i))
            self.endMoveRows()
            return True

        return False

    def sort(self, column: int, order) -> None:
        reverse = (order == Qt.DescendingOrder)
        self.beginResetModel()
        self.list.sort(key=(lambda item: item[column]), reverse=reverse)
        self.endResetModel()

    def add_item(self, item: Merchandise) -> None:
        where = len(self.list)
        self.beginInsertRows(QModelIndex(), where, where)
        self.list.append(item)
        self.endInsertRows()

    def apply_discount(self, value: float) -> None:
        self.beginResetModel()
        for item in filter(lambda item: self.ex.casefold() in item.code.casefold() or (self.ex and self.ex == item.discount_group), self.list):
            item.discount = value
        self.ex = None
        self.endResetModel()

    @Slot(str)
    def select_items(self, ex: str) -> None:
        self.beginResetModel()
        self.ex = ex
        self.endResetModel()

    def get_discount_groups(self) -> typing.Set[str]:
        return set([item.discount_group for item in self.list if item.discount_group is not None])


class DiscountDialog(QtWidgets.QDialog):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self.setWindowTitle(self.tr("Set discounts"))
        icon = QIcon()
        icon.addFile(u":/discount")
        self.setWindowIcon(icon)

        top_level_layout = QtWidgets.QHBoxLayout(self)
        icon_label = QtWidgets.QLabel(self)
        pixmap = QPixmap(":/discount").scaled(128, 128, Qt.KeepAspectRatio)
        icon_label.setPixmap(pixmap)
        top_level_layout.addWidget(icon_label)

        vertical_layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.tr(
            "Please enter regular expression\n"
            "if you want to limit discount to matching items,\n"
            "or leave empty to add discount to all items."
        ))
        vertical_layout.addWidget(self.label)

        self.line_edit_expression = QtWidgets.QLineEdit(self)
        vertical_layout.addWidget(self.line_edit_expression)

        spin_layout = QtWidgets.QHBoxLayout(self)
        spin_layout.addStretch()
        spin_layout.addWidget(QtWidgets.QLabel(self.tr("Discount:"), self))
        self.spinbox_discount = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_discount.setDecimals(1)
        self.spinbox_discount.setMinimum(0)
        self.spinbox_discount.setSingleStep(5)
        self.spinbox_discount.setMaximum(100)
        spin_layout.addWidget(self.spinbox_discount)
        vertical_layout.addLayout(spin_layout)

        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        vertical_layout.addWidget(self.buttons)

        top_level_layout.addLayout(vertical_layout)

    @property
    def discount_value(self) -> float:
        self.spinbox_discount.interpretText()
        return self.spinbox_discount.value()

    @property
    def filter_expression(self) -> str:
        return self.line_edit_expression.text()


class DiscountGroupDialog(QtWidgets.QDialog):
    selectionChanged = Signal(str)

    def __init__(self, groups_list, parent: QObject = None):
        super().__init__(parent)
        self.model = QtCore.QStringListModel(groups_list)

        self.setWindowTitle(self.tr("Set discount value for group"))
        icon = QIcon()
        icon.addFile(u":/discount")
        self.setWindowIcon(icon)

        top_level_layout = QtWidgets.QHBoxLayout(self)
        icon_label = QtWidgets.QLabel(self)
        pixmap = QPixmap(":/discount").scaled(128, 128, Qt.KeepAspectRatio)
        icon_label.setPixmap(pixmap)
        top_level_layout.addWidget(icon_label)

        vertical_layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.tr("Please choose discount group and discount value"))
        vertical_layout.addWidget(self.label)

        self.list_view = QtWidgets.QListView()
        self.list_view.setModel(self.model)
        self.list_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list_view.clicked.connect(self._list_item_clicked)
        vertical_layout.addWidget(self.list_view)

        spin_layout = QtWidgets.QHBoxLayout(self)
        spin_layout.addStretch()
        spin_layout.addWidget(QtWidgets.QLabel(self.tr("Discount:"), self))
        self.spinbox_discount = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_discount.setDecimals(1)
        self.spinbox_discount.setMinimum(0)
        self.spinbox_discount.setSingleStep(5)
        self.spinbox_discount.setMaximum(100)
        spin_layout.addWidget(self.spinbox_discount)
        vertical_layout.addLayout(spin_layout)

        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        vertical_layout.addWidget(self.buttons)

        top_level_layout.addLayout(vertical_layout)

    @property
    def discount_value(self) -> float:
        self.spinbox_discount.interpretText()
        return self.spinbox_discount.value()

    @Slot(QModelIndex)
    def _list_item_clicked(self, index: QModelIndex):
        group = None
        if index.isValid():
            group = self.model.data(index, Qt.DisplayRole)
        self.selectionChanged.emit(group)


class MerchandiseListDelegate(QItemDelegate):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, _, index: QModelIndex) -> QWidget:
        if index.isValid():
            if index.column() == 3:  # discount
                editor = QtWidgets.QDoubleSpinBox(parent)
                editor.setDecimals(1)
                editor.setMinimum(0)
                editor.setSingleStep(5)
                editor.setMaximum(100)
                return editor
            if index.column() == 5:  # count
                editor = QtWidgets.QSpinBox(parent)
                editor.setMinimum(1)
                editor.setMaximum(999999)
                return editor
        return QWidget(parent)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        editor.setValue(index.model().data(index, Qt.EditRole))

    def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        editor.interpretText()
        model.setData(index, editor.value(), Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        editor.setGeometry(option.rect)


class MyStyle(QtWidgets.QProxyStyle):
    def drawPrimitive(self, element, option, painter, widget=None):
        """
        Draw a line across the entire row we're hovering over.
        This may not always work depending on global style
        """
        if element == self.PE_IndicatorItemViewItemDrop and not option.rect.isNull():
            option_new = QtWidgets.QStyleOption(option)
            option_new.rect.setLeft(0)
            option_new.rect.setHeight(1)
            if widget:
                option_new.rect.setRight(widget.width())
            option = option_new
        super().drawPrimitive(element, option, painter, widget)


class MerchandiseListView(QTableView):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.drag_start_row = None
        self.setItemDelegate(MerchandiseListDelegate(self))
        self.setSortingEnabled(False)
        self.setAcceptDrops(True)
        self.setDragDropMode(self.InternalMove)
        self.setDropIndicatorShown(True)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setStyle(MyStyle())

        self.header = super().horizontalHeader()
        self.header.setSortIndicatorShown(False)
        self.header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def setModel(self, model: QtCore.QAbstractItemModel) -> None:
        super().setModel(model)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        if a0.source() is self:
            self.drag_start_row = self.indexAt(a0.pos()).row()
            a0.acceptProposedAction()

    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        drag_end_row = self.indexAt(a0.pos()).row()
        self.model().moveRow(QModelIndex(), self.drag_start_row, QModelIndex(), drag_end_row)
        a0.acceptProposedAction()


class MerchandiseSelectionModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.selected = {}
        self.headers = (
            self.tr("Count"),
            self.tr("Code"),
            self.tr("Description"),
            self.tr("Unit"),
            self.tr("List price"),
        )

    def get_item_id(self, row: int) -> int:
        return self.sourceModel().data(self.createIndex(row, 0), Qt.DisplayRole)

    def get_column_value(self, index: QModelIndex, col: int):
        return self.sourceModel().data(index.sibling(index.row(), col), Qt.DisplayRole)

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        return self.get_column_value(left, 1) < self.get_column_value(right, 1)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return 5

    def data(self, index: QModelIndex, role: int):
        if not index.isValid() or role not in (Qt.DisplayRole, Qt.EditRole, Qt.TextAlignmentRole):
            return

        col = index.column()
        row = index.row()

        if role == Qt.TextAlignmentRole:
            if col > 2:
                return Qt.AlignRight
            return Qt.AlignLeft

        if col == 0:
            item_id = self.get_item_id(row)
            count = self.selected[item_id].count if item_id in self.selected else 0
            if role == Qt.DisplayRole:
                return str(count)
            else:
                return count
        elif col == 4:
            return f"{self.sourceModel().data(index.sibling(index.row(), 5), role):.2f}"
        else:
            return self.sourceModel().data(index, role)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]

    @Slot(str)
    def search(self, ex: str) -> None:
        self.sourceModel().update(ex)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            if index.column() == 0:
                return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled
            return Qt.ItemIsEnabled
        return Qt.NoItemFlags

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if role == Qt.EditRole and index.column() == 0:
            item_id = self.get_item_id(index.row())
            if item_id in self.selected.keys():
                self.selected[item_id].count = value
            elif value > 0:
                item = Merchandise.from_sql_record(self.sourceModel().record(index.row()))
                item.count = value
                self.selected[item.id] = item
            return True
        return False


class MerchandiseSelectionDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> QWidget:
        if index.isValid() and index.column() == 0:
            editor = QtWidgets.QSpinBox(parent)
            editor.setMinimum(0)
            editor.setMaximum(999999)
            return editor
        return QWidget(parent)

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        if index.isValid() and index.column() == 0:
            editor.setValue(index.model().data(index, Qt.EditRole))

    def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        if index.isValid() and index.column() == 0:
            editor.interpretText()
            model.setData(index, editor.value(), Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        editor.setGeometry(option.rect)


class MerchandiseSelectionDialog(QtWidgets.QDialog):
    def __init__(self, model, parent: QObject = None):
        super().__init__(parent)
        self.model = model

        self.setWindowTitle(self.tr("Choose merchandise"))
        self.resize(800, 500)
        self.vertical_layout = QtWidgets.QVBoxLayout(self)

        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.tr("Filter"))
        self.horizontal_layout.addWidget(self.label)
        self.horizontal_layout.addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.push_button_close = QtWidgets.QPushButton(self)
        self.push_button_close.setText(self.tr("Add"))
        self.push_button_close.clicked.connect(super().accept)
        self.horizontal_layout.addWidget(self.push_button_close)
        self.vertical_layout.addLayout(self.horizontal_layout)

        self.line_edit = QtWidgets.QLineEdit(self)
        self.line_edit.textChanged.connect(self.model.search)
        self.vertical_layout.addWidget(self.line_edit)

        self.table_view = QtWidgets.QTableView(self)
        self.table_view.setModel(self.model)
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_view.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.table_view.horizontalHeader().setDefaultSectionSize(60)
        self.table_view.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.table_view.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.table_view.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.table_view.setItemDelegate(MerchandiseSelectionDelegate())
        self.vertical_layout.addWidget(self.table_view)

    @property
    def selected(self) -> Merchandise:
        return self.model.selected

    @classmethod
    def make(cls, parent: QObject = None) -> MerchandiseSelectionDialog:
        logging.debug("Creating %s", cls.__name__)
        sql_model = get_merchandise_sql_model()
        selection_model = MerchandiseSelectionModel(parent)
        selection_model.setSourceModel(sql_model)
        return cls(selection_model, parent)


class CreateMerchandiseDialog(QtWidgets.QDialog):
    def __init__(self, discount_group_model, parent: QObject = None):
        super().__init__(parent)
        self.discount_group_model = discount_group_model

        self.setWindowTitle(self.tr("Create merchandise"))
        self.resize(620, 480)

        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setSpacing(6)
        self.grid_layout.setContentsMargins(11, 11, 11, 11)
        self.grid_layout.setObjectName(u"gridLayout")

        label = QtWidgets.QLabel(self)
        label.setText(self.tr("Code:"))
        self.grid_layout.addWidget(label, 0, 0, 1, 1)
        self.line_edit_code = QtWidgets.QLineEdit(self)
        self.grid_layout.addWidget(self.line_edit_code, 0, 1, 1, 1)

        label = QtWidgets.QLabel(self)
        label.setText(self.tr("Description:"))
        self.grid_layout.addWidget(label, 1, 0, 1, 1)
        self.line_edit_description = QtWidgets.QLineEdit(self)
        self.grid_layout.addWidget(self.line_edit_description, 1, 1, 1, 1)

        label = QtWidgets.QLabel(self)
        label.setText(self.tr("Unit:"))
        self.grid_layout.addWidget(label, 2, 0, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        self.radio_button_metre = QtWidgets.QRadioButton(self.tr("metre"))
        hbox.addWidget(self.radio_button_metre)
        self.radio_button_piece = QtWidgets.QRadioButton(self.tr("piece"))
        self.radio_button_piece.setChecked(True)
        hbox.addWidget(self.radio_button_piece)
        horizontal_spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        hbox.addItem(horizontal_spacer)
        self.grid_layout.addLayout(hbox, 2, 1, 1, 1)

        label = QtWidgets.QLabel(self)
        label.setText(self.tr("Discount group:"))
        self.grid_layout.addWidget(label, 3, 0, 1, 1)
        self.line_edit_discount_group = QtWidgets.QLineEdit(self)
        completer = QtWidgets.QCompleter(self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setModel(self.discount_group_model)
        self.line_edit_discount_group.setCompleter(completer)
        self.grid_layout.addWidget(self.line_edit_discount_group, 3, 1, 1, 1)

        label = QtWidgets.QLabel(self)
        label.setText(self.tr("Price:"))
        self.grid_layout.addWidget(label, 4, 0, 1, 1)
        self.spin_box_price = QtWidgets.QDoubleSpinBox(self)
        self.spin_box_price.setDecimals(2)
        self.spin_box_price.setMinimum(0.0)
        self.spin_box_price.setSingleStep(1.0)
        self.spin_box_price.setMaximum(100000.0)
        spin_layout = QtWidgets.QHBoxLayout()
        spin_layout.addWidget(self.spin_box_price)
        horizontal_spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spin_layout.addItem(horizontal_spacer)
        self.grid_layout.addLayout(spin_layout, 4, 1, 1, 1)

        vertical_spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.grid_layout.addItem(vertical_spacer, 5, 0, 1, 2)

        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.Reset)
        self.button_box.accepted.connect(self.save)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.reset)
        self.grid_layout.addWidget(self.button_box, 6, 0, 1, 2)

    @classmethod
    def make(cls, parent: QObject = None) -> MerchandiseSelectionDialog:
        logging.debug("Creating %s", cls.__name__)
        model = get_discount_groups_model()
        return cls(model, parent)

    @Slot()
    def save(self) -> None:
        try:
            merch_id = create_merchandise(
                self.line_edit_code.text(),
                self.line_edit_description.text(),
                self.radio_button_metre.isChecked(),
                self.line_edit_discount_group.text(),
                self.spin_box_price.value()
            )
        except RuntimeError as e:
            logging.error(f"New merchandise creation failed: {e}")
            QtWidgets.QMessageBox.warning(self, self.tr("Database operation failed"), str(e))
        else:
            logging.info(f"Created new merchandise, id: {merch_id}")
            QtWidgets.QMessageBox.information(self, self.tr("Success"), self.tr("Created new merchandise."))

    @Slot()
    def reset(self) -> None:
        self.line_edit_code.clear()
        self.line_edit_description.clear()
        self.radio_button_piece.setChecked(True)
        self.line_edit_discount_group.clear()
        self.spin_box_price.setValue(0.0)
