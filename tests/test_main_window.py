# pyOffer - program for creating business proposals for purchase of items
# Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

import pytest
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog
from hamcrest import assert_that, is_, none, not_none, empty
from qtmatchers import disabled, enabled

from src.main_window import MainWindow
from src.merchandise import MerchandiseListModel
from src.terms import TermType
from src.user import User
# noinspection PyUnresolvedReferences
from tests.test_customer import sample_customer  # noqa: F401
from tests.test_merchandise import create_merch
from tests.test_terms import create_term_item


@pytest.fixture
def main_window(qtbot, mocker):
    user = mocker.create_autospec(User)
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
    return "X2012N09"


@pytest.fixture
def mock_new_offer(mocker, expected_symbol, expected_next_symbol):
    offer = mocker.patch("src.main_window.Offer", autospec=True)

    def create(author, _parent=None):
        instance = offer.return_value
        instance.author = author
        instance.merchandise_list = mocker.create_autospec(MerchandiseListModel, spec_set=True, instance=True)
        instance.symbol = expected_symbol
        instance.remarks = ""
        instance.terms = {}
        instance.inquiry_number = None
        instance.customer = None

        def update_symbol():
            instance.symbol = expected_next_symbol
        instance.new_symbol.side_effect = update_symbol
        return instance

    offer.create_empty.side_effect = create
    return offer


@pytest.fixture
def active_window(mocker, main_window, mock_new_offer):
    # mock setModel, so it doesn't fail when called with mocked MerchandiseListModel
    mocker.patch.object(main_window.ui.tableView, "setModel")
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

    @pytest.mark.parametrize("menu_name, action_name, slot_name", [
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
    def test_slot_for_triggered(self, mocker, qtbot, active_window, menu_name, action_name, slot_name):
        slot = mocker.patch.object(active_window, f'{slot_name}', autospec=True)
        menu = getattr(active_window.ui, menu_name)
        action = getattr(active_window.ui, action_name)

        with qtbot.wait_signal(action.triggered):
            rect = menu.actionGeometry(action)
            menu.show()
            qtbot.mouseClick(menu, Qt.LeftButton, Qt.NoModifier, rect.center())
        slot.assert_called_once()

    @pytest.mark.parametrize("widget_name, slot_name", [
        pytest.param("command_link_button_customer", "select_customer"),
        pytest.param("command_link_button_delivery", "select_delivery_terms"),
        pytest.param("command_link_button_offer", "select_offer_terms"),
        pytest.param("command_link_button_billing", "select_billing_terms"),
        pytest.param("command_link_button_delivery_date", "select_delivery_date_terms"),
        pytest.param("push_button_add_merchandise", "select_merchandise"),
        pytest.param("push_button_remove_row", "remove_row"),
        pytest.param("push_button_discount", "set_discount"),
    ])
    def test_slot_for_clicked(self, mocker, qtbot, active_window, widget_name, slot_name):
        slot = mocker.patch.object(active_window, f'{slot_name}', autospec=True)
        widget = getattr(active_window.ui, widget_name)

        with qtbot.wait_signal(widget.clicked):
            qtbot.mouseClick(widget, Qt.LeftButton)
        slot.assert_called_once()

    @pytest.mark.parametrize("widget_name, slot_name", [
        pytest.param("check_box_query_date", "inquiry_date_toggled"),
        pytest.param("check_box_query_number", "inquiry_number_toggled"),
    ])
    def test_slot_state_changed(self, mocker, qtbot, active_window, widget_name, slot_name):
        slot = mocker.patch.object(active_window, f'{slot_name}', autospec=True)
        widget = getattr(active_window.ui, widget_name)

        with qtbot.wait_signal(widget.stateChanged):
            qtbot.mouseClick(widget, Qt.LeftButton)
        slot.assert_called_once_with(Qt.Checked)

    @pytest.mark.parametrize("widget_name, slot_name", [
        pytest.param("line_edit_query_number", "inquiry_number_changed"),
        pytest.param("plain_text_edit_remarks", "update_remarks"),
    ])
    def test_slot_text_changed(self, mocker, qtbot, active_window, widget_name, slot_name):
        slot = mocker.patch.object(active_window, f'{slot_name}', autospec=True)
        text = "lorem ipsum"
        widget = getattr(active_window.ui, widget_name)
        widget.setEnabled(True)

        with qtbot.wait_signal(widget.textChanged):
            active_window.ui.tabWidget.setCurrentIndex(1)
            qtbot.keyClicks(widget, text)
        slot.assert_called()
        assert_that(slot.call_count, is_(len(text)))

    def test_new_offer(self, mocker, main_window, expected_symbol, mock_new_offer):
        set_model = mocker.patch.object(main_window.ui.tableView, "setModel", autospec=True)
        assert_that(main_window.offer, is_(none()))
        self._check_offer_ui(main_window, disabled())

        main_window.new_offer()
        mock_new_offer.create_empty.assert_called_once_with(main_window.user, main_window)
        set_model.assert_called_once_with(main_window.offer.merchandise_list)

        assert_that(main_window.windowTitle(), is_(f"pyOffer - {expected_symbol}"))
        assert_that(main_window.offer, is_(not_none()))
        assert_that(main_window.offer.author, is_(main_window.user))
        self._check_offer_ui(main_window, enabled())

    def test_new_offer_symbol(self, active_window, expected_symbol, expected_next_symbol):
        assert_that(active_window.windowTitle(), is_(f"pyOffer - {expected_symbol}"))

        active_window.new_offer_symbol()
        active_window.offer.new_symbol.assert_called_once_with()
        assert_that(active_window.windowTitle(), is_(f"pyOffer - {expected_next_symbol}"))

    def test_select_customer(self, mocker, active_window, sample_customer):
        dialog = mocker.patch("src.main_window.CustomerSelectionDialog", autospec=True)
        dialog.make.return_value = dialog
        dialog.exec_.return_value = QDialog.Accepted
        dialog.chosen_customer = sample_customer

        assert_that(active_window.offer.customer, is_(none()))

        active_window.select_customer()

        dialog.make.assert_called_once_with(active_window)
        dialog.exec_.assert_called_once()
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
    def test_select_terms(self, mocker, active_window, term_type):
        assert_that(active_window.offer.terms, is_({}))
        expected_item = create_term_item(term_type=term_type)
        method_under_test = getattr(active_window, f"select_{term_type.name}_terms")
        ui_under_test = getattr(active_window.ui, f"plain_text_edit_{term_type.name}")

        dialog = mocker.patch("src.main_window.TermsChooserDialog", autospec=True)
        dialog.make.return_value = dialog
        dialog.exec_.return_value = QDialog.Accepted
        dialog.chosen_item = expected_item

        method_under_test()

        dialog.make.assert_called_once_with(term_type, active_window)
        dialog.exec_.assert_called_once()
        assert_that(active_window.offer.terms, is_({term_type: expected_item}))
        assert_that(ui_under_test.toPlainText(), is_(expected_item.long_desc))

    def test_select_1_merchandise(self, mocker, active_window):
        m1 = create_merch(1)

        dialog = mocker.patch("src.main_window.MerchandiseSelectionDialog", autospec=True)
        dialog.make.return_value = dialog
        dialog.exec_.return_value = QDialog.Accepted
        dialog.selected = {m1.id: m1}

        active_window.select_merchandise()

        dialog.make.assert_called_once_with(active_window)
        dialog.exec_.assert_called_once()
        active_window.offer.merchandise_list.change_item_count.assert_called_once_with(m1)

    def test_select_2_merchandise(self, mocker, active_window):
        m1 = create_merch(1)
        m2 = create_merch(2)

        dialog = mocker.patch("src.main_window.MerchandiseSelectionDialog", autospec=True)
        dialog.make.return_value = dialog
        dialog.exec_.return_value = QDialog.Accepted
        dialog.selected = {m1.id: m1, m2.id: m2}

        active_window.select_merchandise()

        dialog.make.assert_called_once_with(active_window)
        dialog.exec_.assert_called_once()
        active_window.offer.merchandise_list.change_item_count.assert_any_call(m1)
        active_window.offer.merchandise_list.change_item_count.assert_any_call(m2)
        assert_that(active_window.offer.merchandise_list.change_item_count.call_count, is_(2))

    @pytest.mark.parametrize("row", [
        pytest.param(0),
        pytest.param(1),
        pytest.param(2),
        pytest.param(3),
    ])
    def test_remove_row(self, mocker, active_window, row):
        row_count = 2
        active_window.offer.merchandise_list.rowCount.return_value = row_count
        current_index = mocker.patch.object(active_window.ui.tableView, "currentIndex", autospec=True)
        current_index.return_value.row.return_value = row
        remove_row = active_window.offer.merchandise_list.removeRow

        active_window.remove_row()
        if row < row_count:
            remove_row.assert_called_once_with(row)
        else:
            remove_row.assert_not_called()

    def test_set_discount(self, mocker, active_window):
        expression = "ex"
        discount = 50
        dialog_class = mocker.patch("src.main_window.DiscountDialog")
        dialog = dialog_class.return_value
        dialog.exec_.return_value = QDialog.Accepted
        dialog.filter_expression = expression
        dialog.discount_value = discount

        active_window.set_discount()

        dialog_class.assert_called_once_with(active_window)
        dialog.exec_.assert_called_once()
        active_window.offer.merchandise_list.set_discount.assert_called_once_with(expression, discount)

    def test_inquiry_number_enabled(self, active_window):
        assert_that(active_window.ui.line_edit_query_number, is_(disabled()))
        assert_that(active_window.ui.line_edit_query_number.text(), is_(empty()))

        active_window.inquiry_number_toggled(Qt.Checked)  # enable
        assert_that(active_window.ui.line_edit_query_number, is_(enabled()))

    def test_inquiry_number_disabled(self, active_window):
        # enable and fill with anything so it can be cleared
        active_window.ui.line_edit_query_number.setEnabled(True)
        active_window.ui.line_edit_query_number.setText("Lorem ipsum")

        active_window.inquiry_number_toggled(Qt.Unchecked)  # disable
        assert_that(active_window.ui.line_edit_query_number, is_(disabled()))
        assert_that(active_window.ui.line_edit_query_number.text(), is_(empty()))

    def test_inquiry_number_changed(self, active_window):
        inquiry = "Lorem ipsum"
        assert_that(active_window.offer.inquiry_number, is_(none()))

        active_window.inquiry_number_changed(inquiry)
        assert_that(active_window.offer.inquiry_number, is_(inquiry))
