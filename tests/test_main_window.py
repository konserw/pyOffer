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
from PySide2.QtWidgets import QDialog
from hamcrest import assert_that, is_, none, not_none, contains_inanyorder
from mock import patch, MagicMock
from qtmatchers import disabled, enabled

from src.main_window import MainWindow
from src.merchandise import MerchandiseListModel
from src.terms import TermType
from src.user import User
# noinspection PyUnresolvedReferences
from tests.test_customer import sample_customer  # noqa: F401
from tests.test_terms import create_term_item
from tests.test_merchandise import create_merch


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
def expected_next_symbol():
    return "X2012N08"


@pytest.fixture
def mock_new_offer(monkeypatch, expected_symbol, expected_next_symbol):
    class MockOffer:
        def __init__(self, author, parent=None):
            self.parent = parent
            self.author = author
            self.symbol = expected_symbol
            self.merchandise_list = MerchandiseListModel()  # MagicMock(spec_set=MerchandiseListModel)
            self.remarks = ""
            self.customer = None
            self.terms = {}

        def new_symbol(self):
            self.symbol = expected_next_symbol

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
            mock.assert_called()
            assert_that(mock.call_count, is_(len(text)))

    def test_new_offer(self, main_window, expected_symbol, mock_new_offer):
        assert_that(main_window.offer, is_(none()))
        self._check_offer_ui(main_window, disabled())

        main_window.new_offer()

        assert_that(main_window.windowTitle(), is_(f"pyOffer - {expected_symbol}"))
        assert_that(main_window.offer, is_(not_none()))
        assert_that(main_window.offer.author, is_(main_window.user))
        self._check_offer_ui(main_window, enabled())
        assert_that(main_window.ui.tableView.model(), is_(main_window.offer.merchandise_list))

    def test_new_offer_symbol(self, monkeypatch, active_window, expected_symbol, expected_next_symbol):
        assert_that(active_window.windowTitle(), is_(f"pyOffer - {expected_symbol}"))

        active_window.new_offer_symbol()
        assert_that(active_window.windowTitle(), is_(f"pyOffer - {expected_next_symbol}"))

    @patch("src.main_window.CustomerSelectionDialog")
    def test_select_customer(self, dialog, active_window, sample_customer):
        dialog.make.return_value = dialog
        dialog.exec.return_value = QDialog.Accepted
        dialog.chosen_customer = sample_customer

        assert_that(active_window.offer.customer, is_(none()))

        active_window.select_customer()

        dialog.make.assert_called_once_with(active_window)
        dialog.exec.assert_called_once()
        assert_that(active_window.offer.customer, is_(sample_customer))
        assert_that(active_window.ui.plain_text_edit_customer.toPlainText(), is_(sample_customer.description))

    def test_update_remarks(self, active_window):
        expected_remarks = "Lorem ipsum"
        assert_that(active_window.offer.remarks, is_(""))
        active_window.ui.plain_text_edit_remarks.setPlainText(expected_remarks)
        active_window.update_remarks()
        assert_that(active_window.offer.remarks, is_(expected_remarks))

    @pytest.mark.parametrize("term_type", [
        pytest.param(TermType.delivery_date),
        pytest.param(TermType.delivery),
        pytest.param(TermType.billing),
        pytest.param(TermType.offer),
    ])
    @patch("src.main_window.TermsChooserDialog")
    def test_select_terms(self, dialog, active_window, term_type):
        assert_that(active_window.offer.terms, is_({}))
        expected_item = create_term_item(term_type=term_type)
        method_under_test = getattr(active_window, f"select_{term_type.name}_terms")
        ui_under_test = getattr(active_window.ui, f"plain_text_edit_{term_type.name}")

        dialog.make.return_value = dialog
        dialog.exec.return_value = QDialog.Accepted
        dialog.chosen_item = expected_item

        method_under_test()

        dialog.make.assert_called_once_with(term_type, active_window)
        dialog.exec.assert_called_once()
        assert_that(active_window.offer.terms, is_({term_type: expected_item}))
        assert_that(ui_under_test.toPlainText(), is_(expected_item.long_desc))

    @patch("src.main_window.MerchandiseSelectionDialog")
    def test_select_merchandise(self, dialog, active_window, sample_customer):
        m1 = create_merch(1)
        m2 = create_merch(2)

        dialog.make.return_value = dialog
        dialog.exec.return_value = QDialog.Accepted
        dialog.selected = {m1.id: m1, m2.id: m2}

        assert_that(active_window.offer.customer, is_(none()))

        active_window.select_merchandise()

        dialog.make.assert_called_once_with(active_window)
        dialog.exec.assert_called_once()
        assert_that(active_window.offer.merchandise_list.list,  contains_inanyorder(m1, m2))
        # todo: dont rely on real MerchandiseListModel, mock it instead and check that change_item_count has been called
