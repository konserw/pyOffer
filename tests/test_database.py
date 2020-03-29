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
import pytest
from PySide2.QtCore import Qt, QModelIndex
from hamcrest import assert_that, is_, none

from src.database import get_merchandise_sql_model, get_merchandise_record, get_user_record, get_new_offer_number


@pytest.mark.usefixtures("db")
class TestMerchandiseRecord:
    def test_1(self):
        rec = get_merchandise_record(1)
        assert_that(rec.field(0).value(), is_(1))
        assert_that(rec.field(1).value(), is_("CODE123"))
        assert_that(rec.field(2).value(), is_("some description"))
        assert_that(rec.field(3).value(), is_("pc."))
        assert_that(rec.field(4).value(), is_(19.99))

    def test_2(self):
        rec = get_merchandise_record(2)
        assert_that(rec.field(0).value(), is_(2))
        assert_that(rec.field(1).value(), is_("CODE456"))
        assert_that(rec.field(2).value(), is_("some other description"))
        assert_that(rec.field(3).value(), is_("m"))
        assert_that(rec.field(4).value(), is_(5.49))

    def test_not_found(self):
        rec = get_merchandise_record(3)
        assert_that(rec, is_(none()))


@pytest.fixture
def merchandise_sql_model():
    return get_merchandise_sql_model()


@pytest.mark.usefixtures("db")
class TestMerchandiseSqlModel:
    def test_data_1(self, merchandise_sql_model):
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(0, 0, QModelIndex()), Qt.DisplayRole), is_(1))  # id
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(0, 1, QModelIndex()), Qt.DisplayRole), is_("CODE123"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(0, 2, QModelIndex()), Qt.DisplayRole), is_("some description"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(0, 3, QModelIndex()), Qt.DisplayRole), is_("pc."))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(0, 4, QModelIndex()), Qt.DisplayRole), is_(19.99))

    def test_data_2(self, merchandise_sql_model):
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(1, 0, QModelIndex()), Qt.DisplayRole), is_(2))  # id
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(1, 1, QModelIndex()), Qt.DisplayRole), is_("CODE456"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(1, 2, QModelIndex()), Qt.DisplayRole), is_("some other description"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(1, 3, QModelIndex()), Qt.DisplayRole), is_("m"))
        assert_that(merchandise_sql_model.data(merchandise_sql_model.index(1, 4, QModelIndex()), Qt.DisplayRole), is_(5.49))

    def test_row_count(self, merchandise_sql_model):
        assert_that(merchandise_sql_model.rowCount(), is_(2))

    def test_column_count(self, merchandise_sql_model):
        assert_that(merchandise_sql_model.columnCount(), is_(5))

    @pytest.mark.parametrize("ex, expected", [
        pytest.param("some desc", 1),
        pytest.param("other", 1),
        pytest.param("123", 1),
        pytest.param("456", 1),
        pytest.param("", 2),
        pytest.param("CODE", 2),
        pytest.param("escr", 2),
        pytest.param("Not found", 0)
    ])
    def test_search(self, merchandise_sql_model, ex, expected):
        assert_that(merchandise_sql_model.rowCount(), is_(2))
        merchandise_sql_model.update(ex)
        assert_that(merchandise_sql_model.rowCount(), is_(expected))


@pytest.mark.usefixtures("db")
class TestUsers:
    @pytest.mark.parametrize("user_id, expected_number", [
        pytest.param(3, 0),  # user 3 does not exist
        pytest.param(1, 1),
        pytest.param(1, 2),
        pytest.param(2, 2323),
        pytest.param(2, 2324),
    ])
    def test_new_offer_number(self, user_id, expected_number):
        """ This test alters database, so it will work only once on clean db"""
        assert_that(get_new_offer_number(user_id), is_(expected_number))

    def test_user_record_1(self):
        rec = get_user_record(1)
        assert_that(rec.value("user_id"), is_(1))
        assert_that(rec.value("name"), is_("Mark Salesman"))
        assert_that(rec.value("mail"), is_("mark@salesman.com"))
        assert_that(rec.value("male"), is_(True))
        assert_that(rec.value("phone"), is_("555 55 55"))
        assert_that(rec.value("char_for_offer_symbol"), is_("M"))
        assert_that(rec.value("business_symbol"), is_("I"))

    def test_user_record_2(self):
        rec = get_user_record(2)
        assert_that(rec.value("user_id"), is_(2))
        assert_that(rec.value("name"), is_("Agatha Salesman"))
        assert_that(rec.value("mail"), is_("agatha@salesman.com"))
        assert_that(rec.value("male"), is_(False))
        assert_that(rec.value("phone"), is_("555 55 50"))
        assert_that(rec.value("char_for_offer_symbol"), is_("A"))
        assert_that(rec.value("business_symbol"), is_("X"))
