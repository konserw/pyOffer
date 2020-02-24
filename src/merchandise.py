from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject


class Merchandise(QObject):
    def __init__(self):
        super().__init__()
        self.id = None
        self.code = None
        self.description = None
        self.listing_price = None
        self.discount = 0
        self.count = 0
        self.by_meter = False  # by default by piece

    @property
    def unit(self):
        if self.by_meter:
            return self.tr("mb.")
        else:
            return self.tr("szt.")

    @property
    def price(self):
        return round(self.listing_price * (100 - self.discount) / 100, 2)

    @property
    def total(self):
        return round(self.price * self.count, 2)

    @staticmethod
    def from_sql_record(record):
        merch = Merchandise()
        merch.id = record.value("merchandise_id")
        merch.code = record.value("code")
        merch.description = record.value("description")
        merch.listing_price = record.value("listing_price")

    def __eq__(self, other):
        return self.id == other.id


class MerchandiseList:
    def __init__(self):
        pass


class MerchandiseListView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
