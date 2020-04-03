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
from datetime import date

import pytest
from PySide2.QtCore import Qt
from hamcrest import assert_that, is_, none, not_none
from mock import patch
from qtmatchers import disabled, enabled

from src.main_window import MainWindow
from src.user import User


@pytest.fixture
def main_window(qtbot):
    user = User()
    user.char_for_offer_symbol = 'N'
    user.business_symbol = 'X'
    main_window = MainWindow(user)
    qtbot.addWidget(main_window)
    main_window.show()
    qtbot.wait_exposed(main_window)
    return main_window


@pytest.fixture
def active_window(main_window, monkeypatch):
    with patch("src.user.date", autospec=True) as mock_date:
        mock_date.today.return_value = date(2020, 12, 15)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        monkeypatch.setattr("src.user.get_new_offer_number", lambda _: 8)
        main_window.new_offer()
    return main_window


class TestMainWindow:
    @staticmethod
    def _check_offer_ui(main_window, expected):
        assert_that(main_window.ui.menu_export, is_(expected))
        assert_that(main_window.ui.action_save, is_(expected))
        assert_that(main_window.ui.action_new_number, is_(expected))
        assert_that(main_window.ui.tab, is_(expected))
        assert_that(main_window.ui.tab_2, is_(expected))

    def test_initial_state(self, main_window):
        assert_that(main_window.windowTitle(), is_("pyOffer"))
        assert_that(main_window.offer, is_(none()))
        assert_that(main_window.user, is_(not_none()))

        assert_that(main_window.ui.action_new, is_(enabled()))
        assert_that(main_window.ui.action_exit, is_(enabled()))
        assert_that(main_window.ui.menu_help, is_(enabled()))

        self._check_offer_ui(main_window, disabled())

    def test_new_offer(self, main_window, monkeypatch):
        assert_that(main_window.offer, is_(none()))
        self._check_offer_ui(main_window, disabled())

        with patch("src.user.date", autospec=True) as mock_date:
            mock_date.today.return_value = date(2020, 12, 15)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            monkeypatch.setattr("src.user.get_new_offer_number", lambda _: 8)
            main_window.new_offer()

        assert_that(main_window.windowTitle(), is_("pyOffer - X2012N08"))
        assert_that(main_window.offer, is_(not_none()))
        assert_that(main_window.offer.author, is_(main_window.user))
        self._check_offer_ui(main_window, enabled())
        assert_that(main_window.ui.tableView.model(), is_(main_window.offer.merchandise_list))

    @pytest.mark.parametrize("menu_name, action_name, slot", [
        pytest.param("menu_offer", "action_new", "new_offer"),
        pytest.param("menu_offer", "action_new_number", "new_offer_symbol"),
    ])
    def test_action_slot_triggered(self, active_window, qtbot, menu_name, action_name, slot):
        menu = getattr(active_window.ui, menu_name)
        action = getattr(active_window.ui, action_name)
        with patch(f"src.main_window.MainWindow.{slot}", autospec=True) as slot_mock:
            with qtbot.wait_signal(action.triggered):
                rect = menu.actionGeometry(action)
                menu.show()
                qtbot.mouseClick(menu, Qt.LeftButton, Qt.NoModifier, rect.center())
            slot_mock.assert_called_once()

    @pytest.mark.parametrize("button_name, slot", [
        pytest.param("command_link_button_customer", "select_customer"),
        pytest.param("command_link_button_delivery", "select_delivery_terms"),
        pytest.param("command_link_button_offer", "select_offer_terms"),
        pytest.param("command_link_button_billing", "select_billing_terms"),
        pytest.param("command_link_button_delivery_date", "select_delivery_date_terms"),
    ])
    def test_slot_triggered(self, active_window, qtbot, button_name, slot):
        button = getattr(active_window.ui, button_name)
        with patch(f"src.main_window.MainWindow.{slot}", autospec=True) as slot_mock:
            with qtbot.wait_signal(button.clicked):
                qtbot.mouseClick(button, Qt.LeftButton)
            slot_mock.assert_called_once()

    def test_x_slot_triggered(self, active_window, qtbot):
        with patch("src.main_window.MainWindow.select_delivery_terms", autospec=True) as mock:
            with qtbot.wait_signal(active_window.ui.command_link_button_delivery.clicked):
                qtbot.mouseClick(active_window.ui.command_link_button_delivery, Qt.LeftButton)
            mock.assert_called_once()


