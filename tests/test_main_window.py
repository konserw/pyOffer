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
from PySide2.QtCore import Qt
from hamcrest import assert_that, is_, none, not_none
from mock import patch
from qtmatchers import disabled, enabled

from src.main_window import MainWindow
from src.merchandise import MerchandiseListModel
from src.user import User


@pytest.fixture
def main_window(qtbot):
    user = User()
    user.char_for_offer_symbol = 'N'
    user.business_symbol = 'X'
    main_window = MainWindow(user)
    qtbot.addWidget(main_window)
    return main_window


@pytest.fixture
def expected_symbol():
    return "X2012N08"


@pytest.fixture
def mock_new_offer(monkeypatch, expected_symbol):
    class MockOffer:
        def __init__(self, author, parent=None):
            self.parent = parent
            self.author = author
            self.symbol = expected_symbol
            self.merchandise_list = MerchandiseListModel()

    monkeypatch.setattr("src.offer.Offer.create_empty", lambda author, parent: MockOffer(author, parent))


@pytest.fixture
def active_window(monkeypatch, main_window, mock_new_offer):
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

    def test_new_offer(self, main_window, expected_symbol, mock_new_offer):
        assert_that(main_window.offer, is_(none()))
        self._check_offer_ui(main_window, disabled())

        main_window.new_offer()

        assert_that(main_window.windowTitle(), is_(f"pyOffer - {expected_symbol}"))
        assert_that(main_window.offer, is_(not_none()))
        assert_that(main_window.offer.author, is_(main_window.user))
        self._check_offer_ui(main_window, enabled())
        assert_that(main_window.ui.tableView.model(), is_(main_window.offer.merchandise_list))

    @pytest.mark.parametrize("menu_name, action_name, slot", [
        pytest.param("menu_offer", "action_new", "new_offer"),
        pytest.param("menu_offer", "action_open", "load_offer"),
        pytest.param("menu_offer", "action_save", "save_offer"),
        pytest.param("menu_offer", "action_new_number", "new_offer_symbol"),
        pytest.param("menu_offer", "action_exit", "exit"),
        pytest.param("menu_export", "action_print", "print_preview"),
        pytest.param("menu_export", "action_PDF", "print_pdf"),
        pytest.param("menu_help", "action_about", "about"),
        pytest.param("menu_help", "action_about_Qt", "about_qt"),
    ])
    def test_slot_for_triggered(self, active_window, qtbot, menu_name, action_name, slot):
        menu = getattr(active_window.ui, menu_name)
        action = getattr(active_window.ui, action_name)
        with patch(f"src.main_window.MainWindow.{slot}", autospec=True) as slot_mock:
            with qtbot.wait_signal(action.triggered):
                rect = menu.actionGeometry(action)
                menu.show()
                qtbot.mouseClick(menu, Qt.LeftButton, Qt.NoModifier, rect.center())
            slot_mock.assert_called_once()

    @pytest.mark.parametrize("widget_name, slot", [
        pytest.param("command_link_button_customer", "select_customer"),
        pytest.param("command_link_button_delivery", "select_delivery_terms"),
        pytest.param("command_link_button_offer", "select_offer_terms"),
        pytest.param("command_link_button_billing", "select_billing_terms"),
        pytest.param("command_link_button_delivery_date", "select_delivery_date_terms"),
        pytest.param("push_button_add_merchandise", "select_merchandise"),
        pytest.param("push_button_remove_row", "remove_row"),
        pytest.param("push_button_discount", "set_discount"),
    ])
    def test_slot_for_clicked(self, active_window, qtbot, widget_name, slot):
        widget = getattr(active_window.ui, widget_name)
        with patch(f"src.main_window.MainWindow.{slot}", autospec=True) as slot_mock:
            with qtbot.wait_signal(widget.clicked):
                qtbot.mouseClick(widget, Qt.LeftButton)
            slot_mock.assert_called_once()

    @pytest.mark.parametrize("widget_name, slot", [
        pytest.param("check_box_query_date", "inquiry_date_toggled"),
        pytest.param("check_box_query_number", "inquiry_number_toggled"),
    ])
    def test_slot_state_changed(self, active_window, qtbot, widget_name, slot):
        widget = getattr(active_window.ui, widget_name)
        with patch(f"src.main_window.MainWindow.{slot}", autospec=True) as mock:
            with qtbot.wait_signal(widget.stateChanged):
                qtbot.mouseClick(widget, Qt.LeftButton)
            mock.assert_called_once_with(active_window, Qt.Checked)

    @pytest.mark.parametrize("widget_name, slot", [
        pytest.param("line_edit_query_number", "inquiry_number_changed"),
        pytest.param("plain_text_edit_remarks", "update_remarks"),
    ])
    def test_slot_text_changed(self, active_window, qtbot, widget_name, slot):
        text = "lorem ipsum"
        widget = getattr(active_window.ui, widget_name)
        widget.setEnabled(True)
        with patch(f"src.main_window.MainWindow.{slot}", autospec=True) as mock:
            with qtbot.wait_signal(widget.textChanged):
                active_window.ui.tabWidget.setCurrentIndex(1)
                qtbot.keyClicks(widget, text)
            #    qtbot.stop()
            mock.assert_called()
            assert_that(mock.call_count, is_(len(text)))
