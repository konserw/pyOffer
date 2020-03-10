import typing
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QWidget, QTableView, QItemDelegate, QDoubleSpinBox, QStyleOptionViewItem
from PyQt5.QtCore import QObject, QAbstractTableModel, QModelIndex, Qt, QVariant, pyqtSlot

from src.database import Database

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

    def set_discount(self, value):
        self.discount = value


class MerchandiseListModel(QAbstractTableModel):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.list = []
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

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.list) + 1

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.headers)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            if section < len(self.list):
                return str(section + 1)
        elif orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self.headers):
            return self.headers[section]
        return QVariant()

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
            return QVariant()

        row = index.row()
        col = index.column()

        if role == Qt.TextAlignmentRole:
            if col > 1:
                return Qt.AlignRight
            return Qt.AlignLeft

        if role == Qt.EditRole and row < len(self.list) and col in (3, 5):
            return self.list[row][col]

        if role == Qt.DisplayRole:
            if row == len(self.list):
                if col == 6:
                    return self.tr("Total:")
                elif col == 7:
                    return str(self.calculate_grand_total())
            elif row < len(self.list):
                return self.list[row][col]

        return QVariant()

    def calculate_grand_total(self):
        sum = 0
        for item in self.list:
            sum += item.total
        return sum

    def supportedDropActions(self) -> Qt.DropActions:
        return Qt.MoveAction

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        default = Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        # if not index.isValid():
        #    return 0
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
            return super().createIndex(row, column, None)
        return super().createIndex(row, column, self.list[row])

    def clear(self):
        if not self.list:
            return

        super().beginRemoveRows(QModelIndex(), 0, len(self.list))
        self.list.clear()
        super().endRemoveRows()

    def change_item_count(self, merchandise_id, count):
        try:
            idx = self.list.index(Merchandise(merchandise_id))
        except ValueError:  # item not on the list
            item = Merchandise.from_sql_record(self.db.get_merchandise_record(merchandise_id))
            item.count = count
            self.list.append(item)
        else:
            self.list[idx].count += count

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        end = row + count - 1
        super().beginRemoveRows(QModelIndex(), row, end)
        for i in range(row, end):
            self.list.pop(i)
        super().endRemoveRows()
        return True

    def moveRows(self, sourceParent: QModelIndex, sourceRow: int, count: int, destinationParent: QModelIndex, destinationChild: int) -> bool:
        if destinationChild in range(sourceRow, sourceRow + count):  # +1 ?
            return False

        last_row = sourceRow + count - 1
        offset = destinationChild - sourceRow
#        if destinationChild == len(self.list):
#            offset -= 1
        super().beginMoveRows(sourceParent, sourceRow, last_row, destinationParent, destinationChild)
        for i in range(count):
            self.list.insert(sourceRow + offset + i, self.list.pop(sourceRow + i))
#TODO: check this
        super().endMoveRows()
        return True

    def sort(self, column, order):
        reverse = (order == Qt.DescendingOrder)
        key = lambda item: item[column]
        super().beginResetModel()
        self.list.sort(key=key, reverse=reverse)
        super().endResetModel()

    def add_item(self, item):
        where = len(self.list)
        super().beginInsertRows(QModelIndex(), where, where)
        self.list.append(item)
        super().endInsertRows()

    def set_discount(self, ex, value):
        map(lambda item: item.set_discount(value), filter(lambda item: ex in item.code, self.list))

    def print(self):
        raise NotImplementedError()


class MerchandiseListDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, _, index: QModelIndex) -> QWidget:
        editor = QDoubleSpinBox(parent)
        editor.setSingleStep(1)
        editor.setMinimum(0)
        if index.column() == 5:
            editor.setMaximum(99999)
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drag_start_index = None
        super().setItemDelegate(MerchandiseListDelegate(self))
        super().setSortingEnabled(True)
        super().setAcceptDrops(True)
        super().setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        super().setDropIndicatorShown(True)
        super().setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.header = super().horizontalHeader()
        self.header.setSortIndicatorShown(False)
        self.header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def setModel(self, model: QtCore.QAbstractItemModel) -> None:
        super().setModel(model)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        if a0.source() is self:
            self.drag_start_index = super().indexAt(a0.pos())
            a0.acceptProposedAction()

    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        drag_end_index = super().indexAt(a0.pos())
        self.model().moveRow(QModelIndex(), self.drag_start_index.row(), QModelIndex, drag_end_index.row())
        a0.acceptProposedAction()


class MerchandiseSelectionModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected = {}
        self.headers = (
            self.tr("Count"),
            self.tr("Code"),
            self.tr("Description"),
            self.tr("List price"),
            self.tr("unit"),
        )

    def get_item_id(self, row):
        return self.sourceModel().data(self.createIndex(row, 0), Qt.DisplayRole)

    def get_column_value(self, index: QModelIndex, col: int):
        return self.sourceModel().data(index.sibling(index.row(), col), Qt.DisplayRole)

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        return self.get_column_value(left, 1) < self.get_column_value(right, 1)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 5

    def data(self, index: QModelIndex, role: int):
        col = index.column()
        if index.isValid() and role == Qt.DisplayRole:
            return self.get_column_value(index, col)
        #if index.isValid() and role == Qt.EditRole and col == 0:
        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]

    @pyqtSlot("QString")
    def search(self, ex):
        self.sourceModel().setFilter("code ilike '%{0}%' or description ilike '%{0}%'".format(ex))

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid() and index.column() == 0:
            return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled
        return Qt.ItemIsEnabled

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if role == Qt.EditRole and index.column() == 0:
            item_id = self.get_item_id(index.row())
            self.selected[item_id] = value
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
            editor.setValue(index.model().data(index, Qt.EditRole).toDouble())

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
        self.horizontal_layout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.push_button_close = QtWidgets.QPushButton(self)
        self.push_button_close.setText(self.tr("Dodaj"))
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
    def selected_items(self):
        return self.model.selected


def create_merchandise_selection_dialog(parent):
    sql_model = Database.get_merchandise_table()
    selection_model = MerchandiseSelectionModel(parent)
    selection_model.setSourceModel(sql_model)
    return MerchandiseSelectionDialog(selection_model, parent)
