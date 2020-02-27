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
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class Database:
    def __init__(self):
        self.database = QSqlDatabase.addDatabase("QPSQL")
        self.database.setHostName("127.0.0.1")
        self.database.setDatabaseName("koferta_test")
        self.database.setUserName("postgres")
        self.database.setPassword("docker")
        if not self.database.open():
            logging.error("Failed to open database")
            logging.error(self.database.lastError().text())
            raise RuntimeError("Failed to connect to db")

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
        model.setTable("terms_{}".format(term_type.name))
        model.select()
        while model.canFetchMore():
            model.fetchMore()
        return model

    @staticmethod
    def get_merchandise_record(merchandise_id):
        model = QSqlTableModel()
        model.setTable("merchandise_view")
        model.setFilter(F"merchandise_id = '{merchandise_id}'")
        model.select()
        return model.record(0)
