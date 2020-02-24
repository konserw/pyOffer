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
import pytest
from hamcrest import assert_that, is_
from PyQt5.QtCore import Qt

from src.database import Database
from src.customer import Customer, CustomerSearchModel


try:
    db = Database()
except:
    pytest.skip("Couldn't connect to database, skipping db tests", allow_module_level=True)


class TestCustomerDB:
    def test_customer_1(self):
        customer_id = 1
        rec = db.get_customer_record(customer_id)
        customer = Customer.from_record(rec)
        assert_that(customer.is_valid, is_(True))
        assert_that(customer.id, is_(customer_id))
        assert_that(customer.short_name, is_("PolImpEx"))
        assert_that(customer.full_name, is_("P.H.U. PolImpEx Sp. z o.o."))
        assert_that(customer.title, is_("Pan"))
        assert_that(customer.first_name, is_("Jan"))
        assert_that(customer.last_name, is_("Kowalski"))
        assert_that(customer.address, is_("Polna 1a/2\n41-300 Dąbrowa Górnicza"))
        assert_that(customer.concated_name, is_("Pan Jan Kowalski"))
        assert_that(customer.html_address, is_("Polna 1a/2<br />\n41-300 Dąbrowa Górnicza"))
        assert_that(customer.db_id, is_("1"))
        assert_that(customer.description, is_(
            "Pan Jan Kowalski\n"
            "P.H.U. PolImpEx Sp. z o.o.\n"
            "Polna 1a/2\n"
            "41-300 Dąbrowa Górnicza"
        ))
        assert_that(str(customer), is_("Customer 1: Pan Jan Kowalski; PolImpEx"))

    def test_customer_2(self):
        customer_id = 2
        rec = db.get_customer_record(customer_id)
        customer = Customer.from_record(rec)
        assert_that(customer.is_valid, is_(True))
        assert_that(customer.id, is_(customer_id))
        assert_that(customer.short_name, is_("PolImpEx"))
        assert_that(customer.full_name, is_("P.H.U. PolImpEx Sp. z o.o."))
        assert_that(customer.title, is_("Pani"))
        assert_that(customer.first_name, is_("Jane"))
        assert_that(customer.last_name, is_("Doe"))
        assert_that(customer.address, is_("Polna 1a/2\n41-300 Dąbrowa Górnicza"))
        assert_that(customer.concated_name, is_("Pani Jane Doe"))
        assert_that(customer.html_address, is_("Polna 1a/2<br />\n41-300 Dąbrowa Górnicza"))
        assert_that(customer.db_id, is_("2"))
        assert_that(customer.description, is_(
            "Pani Jane Doe\n"
            "P.H.U. PolImpEx Sp. z o.o.\n"
            "Polna 1a/2\n"
            "41-300 Dąbrowa Górnicza"
        ))
        assert_that(str(customer), is_("Customer 2: Pani Jane Doe; PolImpEx"))


class TestCustomerSearchModelDB:
    def test_column_headers(self):
        model = CustomerSearchModel()
        assert_that(model.columnCount(), is_(2))
        # todo: other localisations
        assert_that(model.headerData(0, Qt.Horizontal, Qt.DisplayRole), is_("Customer name"))
        assert_that(model.headerData(1, Qt.Horizontal, Qt.DisplayRole), is_("Company name"))

    def test_row_headers(self):
        model = CustomerSearchModel()
        assert_that(model.rowCount(), is_(2))
        assert_that(model.headerData(0, Qt.Vertical, Qt.DisplayRole), is_("0"))
        assert_that(model.headerData(1, Qt.Vertical, Qt.DisplayRole), is_("1"))

    def test_data(self):
        model = CustomerSearchModel()
        assert_that(model.data(model.index(0, 0), Qt.DisplayRole), is_("Pan Jan Kowalski"))
        assert_that(model.data(model.index(0, 1), Qt.DisplayRole), is_("PolImpEx"))
        assert_that(model.data(model.index(1, 0), Qt.DisplayRole), is_("Pani Jane Doe"))
        assert_that(model.data(model.index(1, 1), Qt.DisplayRole), is_("PolImpEx"))

    @staticmethod
    def _test_search_single(pattern):
        model = CustomerSearchModel()
        assert_that(model.rowCount(), is_(2))
        model.search(pattern)
        assert_that(model.rowCount(), is_(1))
        assert_that(model.record(0).value("customer_id"), is_(2))
        model.search("")
        assert_that(model.rowCount(), is_(2))

    @staticmethod
    def _test_search_both(pattern):
        model = CustomerSearchModel()
        assert_that(model.rowCount(), is_(2))
        model.search(pattern)
        assert_that(model.rowCount(), is_(2))

    def test_search_first_name(self):
        pattern = "ne"
        self._test_search_single(pattern)

    def test_search_first_name_both(self):
        pattern = "Jan"
        self._test_search_both(pattern)

    def test_search_last_name(self):
        pattern = "oe"
        self._test_search_single(pattern)

    def test_search_company(self):
        pattern = "Sp. z o.o."
        self._test_search_both(pattern)
