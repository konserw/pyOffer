import typing
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QTableView, QItemDelegate, QDoubleSpinBox
from PyQt5.QtCore import QObject, QAbstractTableModel, QModelIndex, Qt, QVariant


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
            return self.tr("m.")
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
        if count > 0:
            try:
                idx = self.list.index(Merchandise(merchandise_id))
            except ValueError:  # item not on the list
                item = Merchandise.from_sql_record(self.db.get_merchandise_record(merchandise_id))
                item.count = count
                self.list.append(item)
            else:
                self.list[idx].count = count
        else:
            self.list.remove(Merchandise(merchandise_id))

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

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
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
