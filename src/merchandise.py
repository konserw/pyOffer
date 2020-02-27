from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject, QAbstractTableModel, QModelIndex, Qt, QVariant
import typing


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
        if index.isValid() and role == Qt.EditRole and row < len(self.list):
            if col == 3:  # discount
                self.list[row].discount = value
                self.dataChanged.emit(index, index)
                return True
            elif col == 5:  # count
                self.list[row].count = value
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

        if role == Qt.EditRole and row < len(self.list):
            if col == 3:  # discount
                return self.list[row].discount
            elif col == 5:  # count
                return self.list[row].count

        if role == Qt.DisplayRole:
            if row == len(self.list):
                if col == 6:
                    return self.tr("Total:")
                elif col == 7:
                    return str(self.calculate_grand_total())
            elif row < len(self.list):
                if col == 0:
                    return self.list[row].code
                elif col == 1:
                    return self.list[row].description
                elif col == 2:
                    return self.list[row].list_price
                elif col == 3:
                    return self.list[row].discount
                elif col == 4:
                    return self.list[row].price
                elif col == 5:
                    return self.list[row].count
                elif col == 6:
                    return self.list[row].unit
                elif col == 7:
                    return self.list[row].total

        return QVariant()

    def calculate_grand_total(self):
        sum = 0
        for item in self.list:
            sum += item.total
        return sum

    def add_item(self, item):
        row = len(self.list)
        self.beginInsertRows(QModelIndex(), row, row)
        self.list.append(item)

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


class MerchandiseListView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
