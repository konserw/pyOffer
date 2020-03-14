#   kOferta - system usprawniajacy proces ofertowania
#   Copyright (C) 2011  Kamil 'konserw' Strzempowicz, konserw@gmail.com
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see http://www.gnu.org/licenses/
#
import logging
from datetime import date
from PySide2.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel


class Database:
    def __init__(self):
        self.database = QSqlDatabase.addDatabase("QPSQL")
        self.database.setHostName("127.0.0.1")
        self.database.setDatabaseName("koferta_test")
        self.database.setUserName("postgres")
        self.database.setPassword("docker")
        if not self.database.open():
            logging.error("Failed to open database")
            logging.error(f"Plugins: {self.database.drivers()}")
            error = self.database.lastError()
            logging.error(error.text())
            raise RuntimeError(f"Failed to connect to db: {error}")

    @staticmethod
    def get_customer_record(customer_id):
        model = QSqlTableModel()
        model.setTable("customers_view")
        model.setFilter(F"customer_id = '{customer_id}'")
        model.select()
        return model.record(0)

    @staticmethod
    def get_terms_table(term_type):
        model = QSqlTableModel()
        model.setTable(F"terms_{term_type.name}")
        model.select()
        while model.canFetchMore():
            model.fetchMore()
        return model

    @staticmethod
    def get_merchandise_record(merchandise_id):
        text = f"select * from merchandise_view('{date.today()}') where merchandise_id = '{merchandise_id}'"
        query = QSqlQuery(text)
        if not query.next():
            logging.error(f"Query failed: {text}")
            logging.error(query.lastError().text())
        return query.record()

    @staticmethod
    def get_merchandise_table(for_date=date.today()):
        return MerchandiseViewModel(for_date)


class MerchandiseViewModel(QSqlQueryModel):
    def __init__(self, for_date, parent=None):
        super().__init__(parent)
        self.for_date = for_date
        self.update()

    def update(self, ex=""):
        self.beginResetModel()
        self.setQuery(f"select * from merchandise_view('{self.for_date}')"
                      f"where code ilike '%{ex}%' or description ilike '%{ex}%'")
        if self.lastError().isValid():
            raise RuntimeError(self.lastError().text())
        self.endResetModel()
