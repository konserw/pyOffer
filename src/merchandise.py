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
import typing

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import QIcon, QPixmap, QColor
from PySide2.QtCore import QObject, QAbstractTableModel, QModelIndex, Qt, Slot, Signal
from PySide2.QtWidgets import QWidget, QTableView, QItemDelegate, QDoubleSpinBox, QStyleOptionViewItem

from src.database import get_merchandise_sql_model


class Merchandise(QObject):
    def __init__(self, merchandise_id=None):
        super().__init__()
        self.id = merchandise_id
        self.code = None
        self.description = None
        self.list_price = None
        self.discount = 0
        self.count = 0
        self.by_meter = False  # by default by piece
        self.position = None

    @property
    def unit(self):
        if self.by_meter:
            return self.tr("m")
        else:
            return self.tr("pc.")

    @property
    def price(self):
        return round(self.list_price * (100 - self.discount) / 100, 2)

    @property
    def total(self):
        return round(self.price * self.count, 2)

    @staticmethod
    def from_sql_record(record):
        item = Merchandise()
        item.id = record.value("merchandise_id")
        item.code = record.value("code")
        item.description = record.value("description")
        item.list_price = record.value("list_price")
        item.by_meter = record.value("unit") == "m"
        return item

    def __eq__(self, other):
        return self.id == other.id

    def __getitem__(self, col):
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

    def __setitem__(self, key, value):
        if key == 3:
            self.discount = value
        elif key == 5:
            self.count = value
        else:
            raise RuntimeError("unexpected assignment")


class MerchandiseListModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.list = []
        self.ex = None
        self.drag_icon = QPixmap(":/user").scaled(28, 28, Qt.KeepAspectRatio)
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
        if orientation == Qt.Vertical and role == Qt.DecorationRole:
            if section < len(self.list):
                return self.drag_icon
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
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

        if role == Qt.BackgroundRole:
            if self.ex and row < len(self.list) and self.ex.casefold() in self.list[row].code.casefold():
                return QColor(0xFC, 0xF7, 0xBB)

        if role == Qt.EditRole and row < len(self.list) and col in (3, 5):
            return self.list[row][col]

        if role == Qt.DisplayRole:
            if row == len(self.list):
                if col == 6:
                    return self.tr("Total:")
                elif col == 7:
                    return str(self.grand_total)
            elif row < len(self.list):
                return self.list[row][col]

    @property
    def grand_total(self):
        sum = 0
        for item in self.list:
            sum += item.total
        return round(sum, 2)

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

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if row > len(self.list):
            return QModelIndex()
        elif row == len(self.list):
            return self.createIndex(row, column, None)
        return self.createIndex(row, column, self.list[row])

    def clear(self):
        if not self.list:
            return

        self.beginRemoveRows(QModelIndex(), 0, len(self.list))
        self.list.clear()
        self.endRemoveRows()

    def change_item_count(self, item):
        try:
            idx = self.list.index(item)
        except ValueError:  # item not on the list
            self.add_item(item)
        else:
            self.list[idx].count += item.count

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        end = row + count - 1
        self.beginRemoveRows(QModelIndex(), row, end)
        for i in range(row, end + 1):
            self.list.pop(i)
        self.endRemoveRows()
        return True

    def move_item(self, item_index, position):
        self.list[item_index].position = position
#    def moveRows(self, sourceParent: QModelIndex, sourceRow: int, count: int, destinationParent: QModelIndex, destinationChild: int) -> bool:
#        last_row = sourceRow + count - 1
#        offset = destinationChild - sourceRow
#        if destinationChild == len(self.list):
#            offset -= 1
#
#        if destinationChild in range(sourceRow, sourceRow + count + 1):
#            return False
#
#        self.beginMoveRows(sourceParent, sourceRow, last_row, destinationParent, destinationChild)
#        for i in range(count):
#            self.list.insert(sourceRow + offset + i, self.list.pop(sourceRow + i))
#        self.endMoveRows()
#        return True

#    def sort(self, column, order):
#        reverse = (order == Qt.DescendingOrder)
#        self.beginResetModel()
#        self.list.sort(key=(lambda item: item[column]), reverse=reverse)
#        self.endResetModel()

    def add_item(self, item):
        where = len(self.list)
        item.position = where + 1
        self.beginInsertRows(QModelIndex(), where, where)
        self.list.append(item)
        self.endInsertRows()

    def set_discount(self, ex, value):
        self.beginResetModel()
        for item in filter(lambda item: ex.casefold() in item.code.casefold(), self.list):
            item.discount = value
        self.endResetModel()

    @Slot(str)
    def highlight_rows(self, ex):
        self.beginResetModel()
        self.ex = ex
        self.endResetModel()

    def print(self):
        raise NotImplementedError()


class DiscountDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
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
        self.label.setText(self.tr("Please enter regular expression\nif you want to limit discount to matching items,\nor leave empty to add discount to all items."))
        vertical_layout.addWidget(self.label)

        self.line_edit_expression = QtWidgets.QLineEdit(self)
        vertical_layout.addWidget(self.line_edit_expression)

        spin_layout = QtWidgets.QHBoxLayout(self)
        spin_layout.addStretch()
        spin_layout.addWidget(QtWidgets.QLabel(self.tr("Discount:"), self))
        self.spinbox_discount = QtWidgets.QSpinBox(self)
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
    def discount_value(self):
        self.spinbox_discount.interpretText()
        return self.spinbox_discount.value()

    @property
    def filter_expression(self):
        return self.line_edit_expression.text()


class MerchandiseListDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, _, index: QModelIndex) -> QWidget:
        if index.isValid():
            editor = QDoubleSpinBox(parent)
            editor.setSingleStep(1)
            editor.setMinimum(0)
            if index.column() == 5:
                editor.setMaximum(999999)
                return editor
            elif index.column() == 3:
                editor.setMaximum(100)
                return editor
        return QWidget(parent)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        editor.setValue(index.model().data(index, Qt.EditRole))

    def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        editor.interpretText()
        model.setData(index, editor.value(), Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        editor.setGeometry(option.rect)


class MerchandiseListView(QTableView):
    row_moved = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
#        self.drag_start_index = None
        self.setItemDelegate(MerchandiseListDelegate(self))
#        self.setSortingEnabled(True)
#        self.setAcceptDrops(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDropIndicatorShown(True)
#        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.horizontal_header.setSortIndicatorShown(False)
        self.horizontal_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.vertical_header.setSectionsMovable(True)
        self.vertical_header.setFirstSectionMovable(True)
        self.vertical_header.sectionMoved.connect(self.move_row)

    @property
    def horizontal_header(self):
        return self.horizontalHeader()

    @property
    def vertical_header(self):
        return self.verticalHeader()

    def setModel(self, model: QtCore.QAbstractItemModel) -> None:
        super().setModel(model)
        self.horizontal_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    @Slot()
    def move_row(self, logical_index: int, old_visual_index: int, new_visual_index: int) -> None:
        last_row = self.vertical_header.count()
        if old_visual_index < last_row and new_visual_index < last_row:
            self.model().move_item(logical_index, new_visual_index)

            self.row_moved.emit()
        #    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
#        mime = a0.mimeData()
#        x = mime.text()
#        pos = a0.pos()
#        if a0.source() is self:
#            pos = a0.pos()
#            self.drag_start_index = self.indexAt(pos)
#            a0.acceptProposedAction()
#
#    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
#        pos = a0.pos()
#        drag_end_index = self.indexAt(pos)
#        self.model().moveRow(QModelIndex(), self.drag_start_index.row(), QModelIndex(), drag_end_index.row())
#        a0.acceptProposedAction()
#        self.row_moved.emit()


class MerchandiseSelectionModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected = {}
        self.headers = (
            self.tr("Count"),
            self.tr("Code"),
            self.tr("Description"),
            self.tr("Unit"),
            self.tr("List price"),
        )

    def get_item_id(self, row):
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
        col = index.column()
        row = index.row()
        if index.isValid() and col == 0 and role in (Qt.DisplayRole, Qt.EditRole):
            item_id = self.get_item_id(row)
            if item_id in self.selected:
                return self.selected[item_id].count
            return 0
        if index.isValid() and role == Qt.DisplayRole:
            return self.get_column_value(index, col)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]

    @Slot(str)
    def search(self, ex):
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
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> QWidget:
        if index.isValid() and index.column() == 0:
            editor = QDoubleSpinBox(parent)
            editor.setMinimum(0)
            editor.setMaximum(999999)
            editor.setSingleStep(1)
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
    def __init__(self, model, parent=None):
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
    def selected(self):
        return self.model.selected


def create_merchandise_selection_dialog(parent):
    sql_model = get_merchandise_sql_model()
    selection_model = MerchandiseSelectionModel(parent)
    selection_model.setSourceModel(sql_model)
    return MerchandiseSelectionDialog(selection_model, parent)
