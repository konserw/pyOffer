# pyOffer - program for creating business proposals for purchase of items
# Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

from datetime import date

import pytest
from PySide2.QtCore import Qt, QDate, QSizeF
from PySide2.QtGui import QTextDocument
from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog
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
def expected_symbol() -> str:
    return "X2012N08"


@pytest.fixture
def expected_next_symbol() -> str:
    return "X2012N09"


@pytest.fixture
def expected_inquiry_text() -> str:
    return "initial value"


@pytest.fixture
def mock_new_offer(mocker, expected_symbol, expected_next_symbol, expected_inquiry_text):
    offer = mocker.patch("src.main_window.Offer", autospec=True)

    def create(author, _parent=None):
        instance = offer.return_value
        instance.author = author
        instance.merchandise_list = mocker.create_autospec(MerchandiseListModel, spec_set=True, instance=True)
        instance.symbol = expected_symbol
        instance.remarks = ""
        instance.terms = {}
        instance.inquiry_text = expected_inquiry_text
        instance.inquiry_number = None
        instance.inquiry_date = None
        instance.customer = None
        instance.document = "Lorem ipsum"

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

        assert_that(main_window.ui.menu_offer, is_(enabled()))
        assert_that(main_window.ui.action_new, is_(enabled()))
        assert_that(main_window.ui.action_exit, is_(enabled()))
        assert_that(main_window.ui.menu_database, is_(enabled()))
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
        pytest.param("menu_database", "action_create_merchandise", "create_merchandise"),
        pytest.param("menu_help", "action_about", "about"),
        pytest.param("menu_help", "action_about_Qt", "about_qt"),
    ])
    def test_slot_for_triggered(self, mocker, qtbot, active_window, menu_name, action_name, slot_name):
        slot = mocker.patch.object(active_window, slot_name, autospec=True)
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
        pytest.param("push_button_discount_group", "set_discount_group"),
        pytest.param("push_button_query_date", "inquiry_date_button_clicked"),
    ])
    def test_slot_for_clicked(self, mocker, qtbot, active_window, widget_name, slot_name):
        slot = mocker.patch.object(active_window, slot_name, autospec=True)
        widget = getattr(active_window.ui, widget_name)

        with qtbot.wait_signal(widget.clicked):
            qtbot.mouseClick(widget, Qt.LeftButton)
        slot.assert_called_once_with()

    def test_slot_for_calendar(self, mocker, active_window):
        """qtbot.clicked didn't work with calendar for some reason, so I'm left with this simple test"""
        date_changed_slot = mocker.patch.object(active_window, "inquiry_date_changed", autospec=True)

        expected_date = date(2020, 12, 30)
        active_window.calendar.clicked.emit(expected_date)
        date_changed_slot.assert_called_once_with(expected_date)

    @pytest.mark.parametrize("widget_name, slot_name", [
        pytest.param("check_box_query_date", "inquiry_date_toggled"),
        pytest.param("check_box_query_number", "inquiry_number_toggled"),
    ])
    def test_slot_state_changed(self, mocker, qtbot, active_window, widget_name, slot_name):
        slot = mocker.patch.object(active_window, slot_name, autospec=True)
        widget = getattr(active_window.ui, widget_name)

        with qtbot.wait_signal(widget.stateChanged):
            qtbot.mouseClick(widget, Qt.LeftButton)
        slot.assert_called_once_with(Qt.Checked)

    @pytest.mark.parametrize("widget_name, slot_name", [
        pytest.param("line_edit_query_number", "inquiry_number_changed"),
        pytest.param("line_edit_query_date", "inquiry_date_text_changed"),
        pytest.param("plain_text_edit_remarks", "update_remarks"),
    ])
    def test_slot_text_changed(self, mocker, qtbot, active_window, widget_name, slot_name):
        slot = mocker.patch.object(active_window, slot_name, autospec=True)
        text = "lorem ipsum"
        widget = getattr(active_window.ui, widget_name)
        widget.setEnabled(True)

        with qtbot.wait_signal(widget.textChanged):
            active_window.ui.tabWidget.setCurrentIndex(1)
            qtbot.keyClicks(widget, text)
        slot.assert_called()
        assert_that(slot.call_count, is_(len(text)))

    def test_new_offer(self, mocker, main_window, expected_symbol, mock_new_offer, expected_inquiry_text):
        set_model = mocker.patch.object(main_window.ui.tableView, "setModel", autospec=True)
        assert_that(main_window.offer, is_(none()))
        self._check_offer_ui(main_window, disabled())

        main_window.new_offer()
        mock_new_offer.create_empty.assert_called_once_with(main_window.user, main_window)
        set_model.assert_called_once_with(main_window.offer.merchandise_list)

        assert_that(main_window.windowTitle(), is_(f"pyOffer - {expected_symbol}"))
        assert_that(main_window.ui.plain_text_edit_query.toPlainText(), is_(expected_inquiry_text))
        assert_that(main_window.offer, is_(not_none()))
        assert_that(main_window.offer.author, is_(main_window.user))
        self._check_offer_ui(main_window, enabled())

    def test_new_offer_symbol(self, active_window, expected_symbol, expected_next_symbol):
        assert_that(active_window.windowTitle(), is_(f"pyOffer - {expected_symbol}"))

        active_window.new_offer_symbol()
        active_window.offer.new_symbol.assert_called_once_with()
        assert_that(active_window.windowTitle(), is_(f"pyOffer - {expected_next_symbol}"))

    def test_create_merchandise(self, mocker, main_window):
        dialog = mocker.patch("src.main_window.CreateMerchandiseDialog", autospec=True)
        dialog.make.return_value = dialog

        main_window.create_merchandise()

        dialog.make.assert_called_once_with(main_window)
        dialog.show.assert_called_once()

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

    def test_set_discount_accepted(self, mocker, active_window):
        discount = 50
        dialog_class = mocker.patch("src.main_window.DiscountDialog")
        dialog = dialog_class.return_value
        dialog.exec_.return_value = QDialog.Accepted
        dialog.discount_value = discount

        active_window.set_discount()

        dialog_class.assert_called_once_with(active_window)
        dialog.exec_.assert_called_once()
        active_window.offer.merchandise_list.select_items.assert_called_once_with("")
        active_window.offer.merchandise_list.apply_discount.assert_called_once_with(discount)

    def test_set_discount_rejected(self, mocker, active_window):
        dialog_class = mocker.patch("src.main_window.DiscountDialog")
        dialog = dialog_class.return_value
        dialog.exec_.return_value = QDialog.Rejected

        active_window.set_discount()

        dialog_class.assert_called_once_with(active_window)
        dialog.exec_.assert_called_once()
        active_window.offer.merchandise_list.apply_discount.assert_not_called()
        active_window.offer.merchandise_list.select_items.assert_has_calls([mocker.call(''), mocker.call(None)])

    def test_set_discount_group_accepted(self, mocker, active_window):
        discount = 50
        groups = {"group"}
        active_window.offer.merchandise_list.get_discount_groups.return_value = groups
        dialog_class = mocker.patch("src.main_window.DiscountGroupDialog")
        dialog = dialog_class.return_value
        dialog.exec_.return_value = QDialog.Accepted
        dialog.discount_value = discount

        active_window.set_discount_group()

        dialog_class.assert_called_once_with(groups, active_window)
        dialog.exec_.assert_called_once()
        active_window.offer.merchandise_list.apply_discount.assert_called_once_with(discount)

    def test_set_discount_group_rejected(self, mocker, active_window):
        groups = {"group"}
        active_window.offer.merchandise_list.get_discount_groups.return_value = groups
        dialog_class = mocker.patch("src.main_window.DiscountGroupDialog")
        dialog = dialog_class.return_value
        dialog.exec_.return_value = QDialog.Rejected

        active_window.set_discount_group()

        dialog_class.assert_called_once_with(groups, active_window)
        dialog.exec_.assert_called_once()
        active_window.offer.merchandise_list.apply_discount.assert_not_called()
        active_window.offer.merchandise_list.select_items.assert_called_once_with(None)

    def test_inquiry_date_button_clicked(self, mocker, active_window):
        show_calendar = mocker.patch.object(active_window.calendar, 'show', autospec=True)
        assert_that(active_window.ui.check_box_query_date.isChecked(), is_(False))

        active_window.inquiry_date_button_clicked()
        show_calendar.assert_called_once_with()
        assert_that(active_window.ui.check_box_query_date.isChecked(), is_(True))

    def test_inquiry_date_changed(self, mocker, active_window):
        close = mocker.patch.object(active_window.calendar, "close", autospec=True)
        active_window.ui.line_edit_query_date.setEnabled(True)
        assert_that(active_window.ui.line_edit_query_date.text(), is_(empty()))

        active_window.inquiry_date_changed(QDate(2020, 12, 30))
        assert_that(active_window.ui.line_edit_query_date.text(), is_("30.12.2020"))
        close.assert_called_once_with()

    def test_inquiry_date_enabled(self, mocker, active_window):
        mock_date = mocker.patch("src.main_window.date", autospec=True)
        expected_date = date(2020, 12, 30)
        mock_date.today.return_value = expected_date

        assert_that(active_window.ui.line_edit_query_date, is_(disabled()))
        assert_that(active_window.ui.line_edit_query_date.text(), is_(empty()))

        active_window.inquiry_date_toggled(Qt.Checked)  # enable
        assert_that(active_window.ui.line_edit_query_date, is_(enabled()))
        assert_that(active_window.ui.line_edit_query_date.text(), is_("30.12.2020"))

    def test_inquiry_date_disabled(self, active_window):
        active_window.ui.line_edit_query_date.setEnabled(True)
        active_window.ui.line_edit_query_date.setText("lorem ipsum")

        active_window.inquiry_date_toggled(Qt.Unchecked)  # disable
        assert_that(active_window.ui.line_edit_query_date, is_(disabled()))
        assert_that(active_window.ui.line_edit_query_date.text(), is_(empty()))

    @pytest.mark.parametrize("text", [
        pytest.param("30.12.2020"),
        pytest.param("lorem ipsum"),
        pytest.param(""),
    ])
    def test_inquiry_date_text_changed(self, mocker, active_window, text):
        update_inquiry_text = mocker.patch.object(active_window, "update_inquiry_text", autospec=True)
        assert_that(active_window.offer.inquiry_date, is_(none()))

        active_window.inquiry_date_text_changed(text)
        assert_that(active_window.offer.inquiry_date, is_(text))
        update_inquiry_text.assert_called_once_with()

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

    def test_inquiry_number_changed(self, mocker, active_window):
        update_inquiry_text = mocker.patch.object(active_window, "update_inquiry_text", autospec=True)
        inquiry = "Lorem ipsum"
        assert_that(active_window.offer.inquiry_number, is_(none()))

        active_window.inquiry_number_changed(inquiry)
        assert_that(active_window.offer.inquiry_number, is_(inquiry))
        update_inquiry_text.assert_called_once_with()

    def test_update_inquiry_text(self, active_window):
        expected_text = "Lorem ipsum"
        active_window.offer.inquiry_text = expected_text

        active_window.update_inquiry_text()
        assert_that(active_window.ui.plain_text_edit_query.toPlainText(), is_(expected_text))

    def test_print(self, mocker, active_window):
        size = QSizeF(100, 100)
        printer = mocker.create_autospec(QPrinter)
        printer.pageRect.return_value.size.return_value = size
        doc = mocker.create_autospec(QTextDocument, instance=True)
        mocker.patch("src.main_window.QTextDocument").return_value = doc

        active_window.print(printer)

        printer.setPageSize.assert_called_once_with(QPrinter.A4)
        printer.setPageMargins.assert_called_once_with(5, 5, 5, 5, QPrinter.Millimeter)
        printer.setResolution.assert_called_once_with(96)

        doc.setHtml.assert_called_once_with("Lorem ipsum")
        doc.setPageSize.assert_called_once_with(size)
        doc.print_.assert_called_once_with(printer)

    def test_print_preview(self, mocker, active_window):
        dialog = mocker.MagicMock(spec=QPrintPreviewDialog)
        mocker.patch("src.main_window.QPrintPreviewDialog").return_value = dialog
        active_window.print_preview()
        dialog.paintRequested.connect.assert_called_once_with(active_window.print)
        dialog.exec_.assert_called_once_with()

    def test_print_pdf(self, mocker, active_window):
        file_name = "file.pdf"
        mocker.patch("src.main_window.QFileDialog.getSaveFileName").return_value = (file_name, "Portable Document Format (*.pdf)")
        print_mock = mocker.patch.object(active_window, "print")

        active_window.print_pdf()
        print_mock.assert_called_once()
        printer = print_mock.call_args.args[0]
        assert_that(printer.outputFormat(), is_(QPrinter.PdfFormat))
        assert_that(printer.outputFileName(), is_(file_name))
