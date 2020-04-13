#  pyOffer - program for creating business proposals for purchase of items
#  Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation, either version 3 of the License, or any later version.
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#  without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with this program.
#  If not, see <http://www.gnu.org/licenses/>.
#  #
#

import pytest
from hamcrest import assert_that, is_, contains_exactly, empty
from src.database import get_user_record
from src.main_window import MainWindow
from src.user import User
from tests.test_merchandise import create_merch
from PySide2.QtCore import Qt, QPoint


@pytest.mark.e2e
@pytest.mark.usefixtures("db")
class TestEndToEnd:
    @pytest.mark.parametrize("rows, expected", [
        pytest.param([0], "second"),
        pytest.param([1], "first"),
        pytest.param([2], "both"),
        pytest.param([1, 0], "none"),
        pytest.param([0, 0], "none"),
    ])
    def test_remove_row(self, qtbot, rows, expected):
        user = User.from_sql_record(get_user_record(1))
        main_window = MainWindow(user)
        main_window.new_offer()
        m1 = create_merch(1)
        m2 = create_merch(2)
        main_window.offer.merchandise_list.change_item_count(m1)
        main_window.offer.merchandise_list.change_item_count(m2)

        for row in rows:
            x = main_window.ui.tableView.columnViewportPosition(1) + 5
            y = main_window.ui.tableView.rowViewportPosition(row) + 5
            qtbot.mouseClick(main_window.ui.tableView.viewport(), Qt.LeftButton, Qt.NoModifier, QPoint(x, y))
            qtbot.mouseClick(main_window.ui.push_button_remove_row, Qt.LeftButton)

        merch_list = {
            "none": [],
            "first": [m1],
            "second": [m2],
            "both": [m1, m2],
        }
        expected_merch_list = merch_list[expected]
        if expected_merch_list:
            assert_that(main_window.offer.merchandise_list.list, contains_exactly(*expected_merch_list))
        else:
            assert_that(main_window.offer.merchandise_list.list, is_(empty()))

        expected_item_count = len(expected_merch_list)
        assert_that(main_window.ui.tableView.model().rowCount(), is_(expected_item_count + 1))

        total = {
            "none": "0.00",
            "first": "8.99",
            "second": "8.99",
            "both": "17.98",
        }
        expected_grand_total = total[expected]
        x = main_window.ui.tableView.columnViewportPosition(7) + 5
        y = main_window.ui.tableView.rowViewportPosition(expected_item_count) + 5
        grand_total = main_window.ui.tableView.indexAt(QPoint(x, y)).data(Qt.DisplayRole)
        assert_that(grand_total, is_(expected_grand_total))


