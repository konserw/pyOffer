#  pyOffer - program for creating business proposals for purchase of items
#  Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation, either version 3 of the License, or any later version.
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#  without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with this program.
#  If not, see <http://www.gnu.org/licenses/>.
from datetime import date

import pytest
from PySide2.QtCore import Qt, QPoint
from hamcrest import assert_that, is_, none, contains_exactly, empty
from qtmatchers import disabled, enabled

from src.database import get_user_record
from src.main_window import MainWindow
from src.user import User
from tests.test_merchandise import create_merch


@pytest.fixture
def active_window(db):
    user = User.from_sql_record(get_user_record(1))
    window = MainWindow(user)
    window.new_offer()
    return window


@pytest.mark.e2e
class TestEndToEnd:
    @pytest.mark.parametrize("rows, expected", [
        pytest.param([0], "second"),
        pytest.param([1], "first"),
        pytest.param([2], "both"),
        pytest.param([1, 0], "none"),
        pytest.param([0, 0], "none"),
    ])
    def test_remove_row(self, qtbot, active_window, rows, expected):
        m1 = create_merch(1)
        m2 = create_merch(2)
        active_window.offer.merchandise_list.change_item_count(m1)
        active_window.offer.merchandise_list.change_item_count(m2)

        for row in rows:
            x = active_window.ui.tableView.columnViewportPosition(1) + 5
            y = active_window.ui.tableView.rowViewportPosition(row) + 5
            qtbot.mouseClick(active_window.ui.tableView.viewport(), Qt.LeftButton, Qt.NoModifier, QPoint(x, y))
            qtbot.mouseClick(active_window.ui.push_button_remove_row, Qt.LeftButton)

        merch_list = {
            "none": [],
            "first": [m1],
            "second": [m2],
            "both": [m1, m2],
        }
        expected_merch_list = merch_list[expected]
        if expected_merch_list:
            assert_that(active_window.offer.merchandise_list.list, contains_exactly(*expected_merch_list))
        else:
            assert_that(active_window.offer.merchandise_list.list, is_(empty()))

        expected_item_count = len(expected_merch_list)
        assert_that(active_window.ui.tableView.model().rowCount(), is_(expected_item_count + 1))

        total = {
            "none": "0.00",
            "first": "8.99",
            "second": "8.99",
            "both": "17.98",
        }
        expected_grand_total = total[expected]
        x = active_window.ui.tableView.columnViewportPosition(7) + 5
        y = active_window.ui.tableView.rowViewportPosition(expected_item_count) + 5
        grand_total = active_window.ui.tableView.indexAt(QPoint(x, y)).data(Qt.DisplayRole)
        assert_that(grand_total, is_(expected_grand_total))

    def test_inquiry_date_toggled(self, active_window):
        expected_date = f"{date.today():%d.%m.%Y}"

        assert_that(active_window.offer.inquiry_date, is_(none()))
        assert_that(active_window.ui.line_edit_query_date, is_(disabled()))
        assert_that(active_window.ui.line_edit_query_date.text(), is_(empty()))

        active_window.inquiry_date_toggled(Qt.Checked)  # enable
        assert_that(active_window.ui.line_edit_query_date, is_(enabled()))
        assert_that(active_window.ui.line_edit_query_date.text(), is_(expected_date))
        assert_that(active_window.offer.inquiry_date, is_(expected_date))

        active_window.inquiry_date_toggled(Qt.Unchecked)  # disable
        assert_that(active_window.ui.line_edit_query_date, is_(disabled()))
        assert_that(active_window.ui.line_edit_query_date.text(), is_(""))
        assert_that(active_window.offer.inquiry_date, is_(empty()))

    def test_inquiry_number_toggled(self, qtbot, active_window):
        expected_query_number = "Lorem ipsum"
        assert_that(active_window.offer.inquiry_number, is_(none()))
        assert_that(active_window.ui.line_edit_query_number, is_(disabled()))

        active_window.inquiry_number_toggled(Qt.Checked)  # enable
        assert_that(active_window.ui.line_edit_query_number, is_(enabled()))

        # fill with anything
        qtbot.keyClicks(active_window.ui.line_edit_query_number, expected_query_number)
        assert_that(active_window.offer.inquiry_number, is_(expected_query_number))

        active_window.inquiry_number_toggled(Qt.Unchecked)  # disable
        assert_that(active_window.ui.line_edit_query_number, is_(disabled()))
        assert_that(active_window.ui.line_edit_query_number.text(), is_(""))
        assert_that(active_window.offer.inquiry_number, is_(empty()))
