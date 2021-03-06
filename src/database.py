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
import os
import sys
from datetime import date

from PySide2.QtCore import QObject, Qt
from PySide2.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel, QSqlRecord


def connect(host_name: str, database_name: str, user_name: str, password: str, port: int = 5432) -> None:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    database = QSqlDatabase.addDatabase("QPSQL")
    database.setHostName(host_name)
    database.setDatabaseName(database_name)
    database.setUserName(user_name)
    database.setPassword(password)
    database.setPort(port)
    if not database.open():
        logging.error("Failed to open database")
        logging.error("Plugins: %s", database.drivers())
        error = database.lastError()
        logging.error(error.driverText())
        logging.error(error.databaseText())
        raise RuntimeError("Failed to open database", error.driverText(), error.databaseText())
    logging.info("Database opened successfully")


def get_customer_record(customer_id: int) -> QSqlRecord:
    model = QSqlTableModel()
    model.setTable("customers")
    model.setFilter(F"customer_id = '{customer_id}'")
    model.select()
    return model.record(0)


def get_users_table() -> QSqlTableModel:
    model = QSqlTableModel()
    model.setTable("users")
    model.setSort(0, Qt.AscendingOrder)
    model.select()
    return model


def get_user_record(user_id: int) -> QSqlRecord:
    model = get_users_table()
    model.setFilter(F"user_id = '{user_id}'")
    return model.record(0)


def get_new_offer_number(user_id: int) -> int:
    text = f"SELECT public.get_new_offer_number({user_id})"
    query = QSqlQuery(text)
    if not query.next():
        logging.error(f"Query failed: {text}")
        logging.error(query.lastError().text())
        raise RuntimeError("Error accessing database")
    return query.record().value(0)


def get_var(key: str) -> str:
    text = f"SELECT value FROM public.vars WHERE key = '{key}'"
    query = QSqlQuery(text)
    if not query.next():
        logging.error(f"Query failed: {text}")
        logging.error(query.lastError().text())
        raise RuntimeError("Error accessing database")
    record = query.record()
    return record.value("value")


def get_terms_table(term_type: int) -> QSqlTableModel:
    model = QSqlTableModel()
    model.setTable("terms")
    model.setFilter(f"term_type = {term_type}")
    model.removeColumn(1)  # remove term_type column as it no longer carries any value
    model.select()
    while model.canFetchMore():
        model.fetchMore()
    return model


def get_merchandise_record(merchandise_id: int) -> QSqlRecord:
    text = f"select * from merchandise_view('{date.today()}') where merchandise_id = '{merchandise_id}'"
    query = QSqlQuery(text)
    if not query.next():
        logging.error(f"Query failed: {text}")
        logging.error(query.lastError().text())
        raise RuntimeError("Error accessing database")
    return query.record()


class MerchandiseSqlModel(QSqlQueryModel):
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


def get_merchandise_sql_model(for_date: date = date.today()) -> MerchandiseSqlModel:
    return MerchandiseSqlModel(for_date)


def get_discount_groups_model(parent: QObject = None) -> QSqlQueryModel:
    model = QSqlQueryModel(parent)
    model.setQuery("SELECT distinct discount_group FROM public.merchandise;")
    if model.lastError().isValid():
        raise RuntimeError(model.lastError().text())
    return model


def create_merchandise(code: str, description: str, by_metre: bool, discount_group: str, price: float) -> int:
    unit = 'm' if by_metre else 'pc.'
    query_text = f"SELECT public.create_merchandise('{code}', '{description}', '{unit}', '{discount_group}', {price})"
    query = QSqlQuery(query_text)
    if not query.next():
        raise RuntimeError(f"Query {query_text} failed with:\n{query.lastError().text()}")
    merchandise_id = query.value(0)
    if merchandise_id < 0:
        raise RuntimeError(f"Query {query_text} failed on server side")
    return merchandise_id


def create_customer(title: str, first_name: str, last_name: str, company_name: str, address: str) -> None:
    query_text = f"""
INSERT INTO public.customers(title, first_name, last_name, company_name, address)
    VALUES ('{title}', '{first_name}', '{last_name}', '{company_name}', '{address}')
;"""
    query = QSqlQuery()
    if not query.exec_(query_text):
        raise RuntimeError(f"Query {query_text} failed with:\n{query.lastError().text()}")


def get_company_names_model(parent: QObject = None) -> QSqlQueryModel:
    model = QSqlQueryModel(parent)
    model.setQuery("SELECT distinct company_name FROM public.customers;")
    if model.lastError().isValid():
        raise RuntimeError(model.lastError().text())
    return model


def get_addresses_model(parent: QObject = None) -> QSqlQueryModel:
    model = QSqlQueryModel(parent)
    model.setQuery("SELECT distinct address FROM public.customers;")
    if model.lastError().isValid():
        raise RuntimeError(model.lastError().text())
    return model
