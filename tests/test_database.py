# pyOffer - program for creating business proposals for purchase of items
# Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

from contextlib import contextmanager
from decimal import Decimal

import pytest
from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtSql import QSqlDatabase, QSqlQuery
from hamcrest import assert_that, is_, calling, raises

from src.terms import TermType


@contextmanager
def rollback():
    database = QSqlDatabase.database()
    database.transaction()
    try:
        yield database
    finally:
        database.rollback()


class TestCustomer:
    @pytest.mark.parametrize("title, first_name, last_name, company_name, address", [
        pytest.param("", "", "", "", ""),
        pytest.param("mr", "John", "Smith", "some company", "some street 2\nSome Town"),
        pytest.param("ms", "Jane", "Doe", "some other company", "Some other ave. 116/4\nAnother Town"),
    ])
    def test_can_create_customer(self, db, title, first_name, last_name, company_name, address):
        with rollback():
            db.create_customer(title, first_name, last_name, company_name, address)

            query = QSqlQuery("SELECT currval('customers_customer_id_seq');")
            if not query.next():
                raise AssertionError(f"Couldn't retrieve customer_id: {query.lastError().text()}")
            customer_id = query.value(0)

            rec = db.get_customer_record(customer_id)
            assert_that(rec.field(0).value(), is_(customer_id))
            assert_that(rec.field(1).value(), is_(title))
            assert_that(rec.field(2).value(), is_(first_name))
            assert_that(rec.field(3).value(), is_(last_name))
            assert_that(rec.field(4).value(), is_(company_name))
            assert_that(rec.field(5).value(), is_(address))


class TestMerchandise:
    @pytest.mark.parametrize("code, desc, unit, group, price", [
        pytest.param("test_code", "test_desc", "m", "some_group", 9.99),
        pytest.param("test_code", "test_desc", "pc.", "some_group", 9.99),
        pytest.param("", "", "pc.", "", 0),
        pytest.param("test_code", "test_desc", "m", "some_group", 100000.0),
    ])
    def test_can_create_merchandise(self, db, code, desc, unit, group, price):
        with rollback():
            by_metre = unit == "m"
            merchandise_id = db.create_merchandise(code, desc, by_metre, group, Decimal(price))

            rec = db.get_merchandise_record(merchandise_id)
            assert_that(rec.field(0).value(), is_(merchandise_id))
            assert_that(rec.field(1).value(), is_(code))
            assert_that(rec.field(2).value(), is_(desc))
            assert_that(rec.field(3).value(), is_(unit))
            assert_that(rec.field(4).value(), is_(group))
            assert_that(rec.field(5).value(), is_(price))

    @pytest.mark.parametrize("price", [
        pytest.param(None),
        pytest.param("x"),
        pytest.param(1000000.0),
    ])
    def test_create_merchandise_throws(self, db, price):
        with rollback():
            assert_that(
                calling(db.create_merchandise).with_args("test_code", "test_desc", "m", "", price),
                raises(RuntimeError, "Query .* failed")
            )

    def test_get_discount_groups_model(self, db):
        model = db.get_discount_groups_model()

        assert_that(model.rowCount(), is_(2))
        groups_in_model = {model.data(model.index(0, 0), Qt.DisplayRole), model.data(model.index(1, 0), Qt.DisplayRole)}
        assert_that(groups_in_model, is_({"group1", "group2"}))

    def test_record_1(self, db):
        rec = db.get_merchandise_record(1)
        assert_that(rec.field(0).value(), is_(1))
        assert_that(rec.field(1).value(), is_("CODE123"))
        assert_that(rec.field(2).value(), is_("some description"))
        assert_that(rec.field(3).value(), is_("pc."))
        assert_that(rec.field(4).value(), is_("group1"))
        assert_that(rec.field(5).value(), is_(19.99))

    def test_record_2(self, db):
        rec = db.get_merchandise_record(2)
        assert_that(rec.field(0).value(), is_(2))
        assert_that(rec.field(1).value(), is_("CODE456"))
        assert_that(rec.field(2).value(), is_("some other description"))
        assert_that(rec.field(3).value(), is_("m"))
        assert_that(rec.field(4).value(), is_("group2"))
        assert_that(rec.field(5).value(), is_(5.49))

    def test_record_3(self, db):
        rec = db.get_merchandise_record(3)
        assert_that(rec.field(0).value(), is_(3))
        assert_that(rec.field(1).value(), is_("CODE789"))
        assert_that(rec.field(2).value(), is_("Yet another description"))
        assert_that(rec.field(3).value(), is_("pc."))
        assert_that(rec.field(4).value(), is_("group1"))
        assert_that(rec.field(5).value(), is_(120))

    def test_record_not_found(self, db):
        assert_that(calling(db.get_merchandise_record).with_args(13), raises(RuntimeError))


@pytest.fixture
def merchandise_sql_model(db):
    return db.get_merchandise_sql_model()


class TestMerchandiseSqlModel:
    def test_data_1(self, merchandise_sql_model):
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(0, 0, QModelIndex()), Qt.DisplayRole), is_(1))  # id
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(0, 1, QModelIndex()), Qt.DisplayRole), is_("CODE123"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(0, 2, QModelIndex()), Qt.DisplayRole), is_("some description"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(0, 3, QModelIndex()), Qt.DisplayRole), is_("pc."))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(0, 4, QModelIndex()), Qt.DisplayRole), is_("group1"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(0, 5, QModelIndex()), Qt.DisplayRole), is_(19.99))

    def test_data_2(self, merchandise_sql_model):
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(1, 0, QModelIndex()), Qt.DisplayRole), is_(2))  # id
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(1, 1, QModelIndex()), Qt.DisplayRole), is_("CODE456"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(1, 2, QModelIndex()), Qt.DisplayRole), is_("some other description"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(1, 3, QModelIndex()), Qt.DisplayRole), is_("m"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(1, 4, QModelIndex()), Qt.DisplayRole), is_("group2"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(1, 5, QModelIndex()), Qt.DisplayRole), is_(5.49))

    def test_data_3(self, merchandise_sql_model):
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(2, 0, QModelIndex()), Qt.DisplayRole), is_(3))  # id
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(2, 1, QModelIndex()), Qt.DisplayRole), is_("CODE789"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(2, 2, QModelIndex()), Qt.DisplayRole), is_("Yet another description"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(2, 3, QModelIndex()), Qt.DisplayRole), is_("pc."))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(2, 4, QModelIndex()), Qt.DisplayRole), is_("group1"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(2, 5, QModelIndex()), Qt.DisplayRole), is_(120))

    def test_row_count(self, merchandise_sql_model):
        assert_that(merchandise_sql_model.rowCount(), is_(3))

    def test_column_count(self, merchandise_sql_model):
        assert_that(merchandise_sql_model.columnCount(), is_(6))

    @pytest.mark.parametrize("ex, expected", [
        pytest.param("some desc", 1),
        pytest.param("other", 2),
        pytest.param("123", 1),
        pytest.param("456", 1),
        pytest.param("789", 1),
        pytest.param("", 3),
        pytest.param("CODE", 3),
        pytest.param("escr", 3),
        pytest.param("Not found", 0)
    ])
    def test_search(self, merchandise_sql_model, ex, expected):
        assert_that(merchandise_sql_model.rowCount(), is_(3))
        merchandise_sql_model.update(ex)
        assert_that(merchandise_sql_model.rowCount(), is_(expected))


class TestUsers:
    @pytest.mark.parametrize("user_id, expected_number", [
        pytest.param(3, 0),  # user 3 does not exist
        pytest.param(1, 1),
        pytest.param(2, 2323),
    ])
    def test_new_offer_number(self, db, user_id, expected_number):
        with rollback():
            assert_that(db.get_new_offer_number(user_id), is_(expected_number))

    @pytest.mark.parametrize("user_id, expected_number", [
        pytest.param(1, 1),
        pytest.param(2, 2323),
    ])
    def test_new_offer_number_double(self, db, user_id, expected_number):
        with rollback():
            assert_that(db.get_new_offer_number(user_id), is_(expected_number))
            assert_that(db.get_new_offer_number(user_id), is_(expected_number+1))

    def test_user_record_1(self, db):
        rec = db.get_user_record(1)
        assert_that(rec.value("user_id"), is_(1))
        assert_that(rec.value("name"), is_("Mark Salesman"))
        assert_that(rec.value("mail"), is_("mark@salesman.com"))
        assert_that(rec.value("male"), is_(True))
        assert_that(rec.value("phone"), is_("555 55 55"))
        assert_that(rec.value("char_for_offer_symbol"), is_("M"))
        assert_that(rec.value("business_symbol"), is_("I"))

    def test_user_record_2(self, db):
        rec = db.get_user_record(2)
        assert_that(rec.value("user_id"), is_(2))
        assert_that(rec.value("name"), is_("Agatha Salesman"))
        assert_that(rec.value("mail"), is_("agatha@salesman.com"))
        assert_that(rec.value("male"), is_(False))
        assert_that(rec.value("phone"), is_("555 55 50"))
        assert_that(rec.value("char_for_offer_symbol"), is_("A"))
        assert_that(rec.value("business_symbol"), is_("X"))


class TestTerms:
    def test_billing_terms_table(self, db):
        model = db.get_terms_table(TermType.billing.value)
        assert_that(model.tableName(), is_("terms"))
        assert_that(model.rowCount(), is_(15))
        assert_that(model.columnCount(), is_(3))
        rec = model.record()
        assert_that(rec.fieldName(0), is_("term_id"))
        assert_that(rec.fieldName(1), is_("short_desc"))
        assert_that(rec.fieldName(2), is_("long_desc"))

    def test_delivery_terms_table(self, db):
        model = db.get_terms_table(TermType.delivery.value)
        assert_that(model.tableName(), is_("terms"))
        assert_that(model.rowCount(), is_(14))
        assert_that(model.columnCount(), is_(3))
        rec = model.record()
        assert_that(rec.fieldName(0), is_("term_id"))
        assert_that(rec.fieldName(1), is_("short_desc"))
        assert_that(rec.fieldName(2), is_("long_desc"))

    def test_delivery_date_terms_table(self, db):
        model = db.get_terms_table(TermType.delivery_date.value)
        assert_that(model.tableName(), is_("terms"))
        assert_that(model.rowCount(), is_(27))
        assert_that(model.columnCount(), is_(3))
        rec = model.record()
        assert_that(rec.fieldName(0), is_("term_id"))
        assert_that(rec.fieldName(1), is_("short_desc"))
        assert_that(rec.fieldName(2), is_("long_desc"))

    def test_offer_terms_table(self, db):
        model = db.get_terms_table(TermType.offer.value)
        assert_that(model.tableName(), is_("terms"))
        assert_that(model.rowCount(), is_(4))
        assert_that(model.columnCount(), is_(3))
        rec = model.record()
        assert_that(rec.fieldName(0), is_("term_id"))
        assert_that(rec.fieldName(1), is_("short_desc"))
        assert_that(rec.fieldName(2), is_("long_desc"))

    @pytest.mark.parametrize("key, expected_value", [
        pytest.param("order email", "biuro.pl@aliaxis.com")
    ])
    def test_get_var(self, db, key, expected_value):
        value = db.get_var(key)
        assert_that(value, is_(expected_value))


class TestNoConnection:
    @pytest.mark.skip("this test breaks other tests using db")
    def test_connect_failed(self, db):
        assert_that(calling(db.connect).with_args("127.0.0.1", "name", "name", "pass"), raises(RuntimeError, "Failed to connect to db"))
