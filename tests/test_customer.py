# pyOffer - program for creating business proposals for purchase of items
# Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

from unittest.mock import MagicMock

import pytest
from PySide2.QtCore import Qt, QPoint, QStringListModel
from PySide2.QtSql import QSqlRecord
from PySide2.QtWidgets import QDialog, QDialogButtonBox
from hamcrest import assert_that, is_, not_none, empty

from src.customer import Customer, CustomerSearchModel, CustomerSelectionDialog, CustomerSearchWidget, CreateCustomerDialog

CUSTOMER_ID = 1
COMPANY_NAME = "Full business name that is quite long"
TITLE = "Mr."
FIRST_NAME = "John"
LAST_NAME = "Doe"
ADDRESS = "255 Some street\nIn some town"


@pytest.fixture
def sample_customer():
    c = Customer()
    c.id = CUSTOMER_ID
    c.company_name = COMPANY_NAME
    c.title = TITLE
    c.first_name = FIRST_NAME
    c.last_name = LAST_NAME
    c.address = ADDRESS
    return c


class TestCustomer:
    def test_customer_from_record(self):
        record = MagicMock(spec_set=QSqlRecord)
        record.value.side_effect = lambda key: {
            "customer_id": CUSTOMER_ID,
            "company_name": COMPANY_NAME,
            "title": TITLE,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "address": "255 Some street\\nIn some town",
        }[key]

        customer = Customer.from_record(record)
        assert_that(customer.is_valid, is_(True))
        assert_that(customer.id, is_(CUSTOMER_ID))
        assert_that(customer.company_name, is_(COMPANY_NAME))
        assert_that(customer.title, is_(TITLE))
        assert_that(customer.last_name, is_(LAST_NAME))
        assert_that(customer.address, is_(ADDRESS))

    def test_concated_name(self, sample_customer):
        assert_that(sample_customer.concated_name, is_("Mr. John Doe"))

    def test_is_not_valid(self):
        customer = Customer()
        assert_that(customer.is_valid, is_(False))

    def test_html_address(self, sample_customer):
        assert_that(sample_customer.html_address, is_("255 Some street<br />\nIn some town"))

    def test_db_id(self, sample_customer):
        assert_that(sample_customer.db_id, is_("1"))

    def test_null_id(self):
        customer = Customer()
        assert_that(customer.db_id, is_("NULL"))

    def test_description(self, sample_customer):
        assert_that(sample_customer.description, is_("Mr. John Doe\nFull business name that is quite long\n255 Some street\nIn some town"))

    def test_str(self, sample_customer):
        assert_that(str(sample_customer), is_("<Customer 1: Mr. John Doe; Full business name that is quite long>"))

    def test_customer_from_db_1(self, db):
        customer_id = 1
        rec = db.get_customer_record(customer_id)
        customer = Customer.from_record(rec)

        assert_that(customer.is_valid, is_(True))
        assert_that(customer.id, is_(customer_id))
        assert_that(customer.company_name, is_("P.H.U. PolImpEx Sp. z o.o."))
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
        assert_that(str(customer), is_("<Customer 1: Pan Jan Kowalski; P.H.U. PolImpEx Sp. z o.o.>"))

    def test_customer_from_db_2(self, db):
        customer_id = 2
        rec = db.get_customer_record(customer_id)
        customer = Customer.from_record(rec)

        assert_that(customer.is_valid, is_(True))
        assert_that(customer.id, is_(customer_id))
        assert_that(customer.company_name, is_("P.H.U. PolImpEx Sp. z o.o."))
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
        assert_that(str(customer), is_("<Customer 2: Pani Jane Doe; P.H.U. PolImpEx Sp. z o.o.>"))


@pytest.mark.usefixtures("db")
class TestCustomerSearchModel:
    def setup_method(self):
        self.model = CustomerSearchModel()

    def test_column_headers(self):
        assert_that(self.model.columnCount(), is_(3))
        # todo: other localisations
        assert_that(self.model.headerData(0, Qt.Horizontal, Qt.DisplayRole), is_("Customer name"))
        assert_that(self.model.headerData(1, Qt.Horizontal, Qt.DisplayRole), is_("Company name"))
        assert_that(self.model.headerData(2, Qt.Horizontal, Qt.DisplayRole), is_("Address"))

    def test_row_headers(self):
        assert_that(self.model.rowCount(), is_(2))
        assert_that(self.model.headerData(0, Qt.Vertical, Qt.DisplayRole), is_("0"))
        assert_that(self.model.headerData(1, Qt.Vertical, Qt.DisplayRole), is_("1"))

    def test_data(self):
        assert_that(self.model.data(self.model.index(0, 0), Qt.DisplayRole), is_("Pan Jan Kowalski"))
        assert_that(self.model.data(self.model.index(0, 1), Qt.DisplayRole), is_("P.H.U. PolImpEx Sp. z o.o."))
        assert_that(self.model.data(self.model.index(0, 2), Qt.DisplayRole), is_("Polna 1a/2\n41-300 Dąbrowa Górnicza"))
        assert_that(self.model.data(self.model.index(1, 0), Qt.DisplayRole), is_("Pani Jane Doe"))
        assert_that(self.model.data(self.model.index(1, 1), Qt.DisplayRole), is_("P.H.U. PolImpEx Sp. z o.o."))
        assert_that(self.model.data(self.model.index(1, 2), Qt.DisplayRole), is_("Polna 1a/2\n41-300 Dąbrowa Górnicza"))

    def _test_search_single(self, pattern):
        assert_that(self.model.rowCount(), is_(2))
        self.model.search(pattern)
        assert_that(self.model.rowCount(), is_(1))
        assert_that(self.model.record(0).value("customer_id"), is_(2))
        self.model.search("")
        assert_that(self.model.rowCount(), is_(2))

    def _test_search_both(self, pattern):
        assert_that(self.model.rowCount(), is_(2))
        self.model.search(pattern)
        assert_that(self.model.rowCount(), is_(2))

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

    def test_with_modeltester(self, qtmodeltester):
        qtmodeltester.check(self.model)


@pytest.mark.usefixtures("db")
class TestCustomerSearchWidget:
    def test_initial_state(self, qtbot):
        model = CustomerSearchModel()
        widget = CustomerSearchWidget(model)
        qtbot.addWidget(widget)

        assert_that(widget.line_edit.text(), is_(""))
        assert_that(widget.chosen_customer, is_(None))

    @pytest.mark.parametrize("row, expected", [
        pytest.param(0, "Pan Jan Kowalski"),
        pytest.param(1, "Pani Jane Doe")
    ])
    def test_selection_changed(self, qtbot, row, expected):
        model = CustomerSearchModel()
        widget = CustomerSearchWidget(model)
        qtbot.addWidget(widget)

        pos = QPoint(widget.table_widget.columnViewportPosition(1), widget.table_widget.rowViewportPosition(row))
        qtbot.mouseClick(widget.table_widget.viewport(), Qt.LeftButton, pos=pos)

        assert_that(widget.chosen_customer, is_(not_none()))
        assert_that(widget.chosen_customer.concated_name, is_(expected))

    def test_search(self, qtbot):
        model = CustomerSearchModel()
        widget = CustomerSearchWidget(model)
        qtbot.addWidget(widget)

        assert_that(model.rowCount(), is_(2))
        qtbot.keyClicks(widget.line_edit, "ne")

        assert_that(widget.line_edit.text(), is_("ne"))
        assert_that(model.rowCount(), is_(1))
        assert_that(model.record(0).value("customer_id"), is_(2))


@pytest.mark.usefixtures("db")
class TestCustomerSelectionDialog:
    def test_initial_state(self, qtbot):
        dialog = CustomerSelectionDialog.make()
        qtbot.addWidget(dialog)

        # todo: translations
        assert_that(dialog.push_button_exit.text(), is_("OK"))
        assert_that(dialog.windowTitle(), is_("Select customer"))

    def test_button_accepts(self, qtbot):
        dialog = CustomerSelectionDialog.make()
        qtbot.addWidget(dialog)

        qtbot.mouseClick(dialog.push_button_exit, Qt.LeftButton)
        assert_that(dialog.result(), is_(QDialog.Accepted))

    @pytest.mark.parametrize("row, expected", [
        pytest.param(0, "Pan Jan Kowalski"),
        pytest.param(1, "Pani Jane Doe")
    ])
    def test_selection_changed(self, qtbot, row, expected):
        dialog = CustomerSelectionDialog.make()
        qtbot.addWidget(dialog)

        pos = QPoint(dialog.customer_search.table_widget.columnViewportPosition(1), dialog.customer_search.table_widget.rowViewportPosition(row))
        qtbot.mouseClick(dialog.customer_search.table_widget.viewport(), Qt.LeftButton, pos=pos)

        assert_that(dialog.chosen_customer, is_(not_none()))
        assert_that(dialog.chosen_customer.concated_name, is_(expected))


@pytest.fixture
def create_customer_dialog(qtbot):
    dialog = CreateCustomerDialog(QStringListModel(["company"]), QStringListModel(["address"]))
    qtbot.addWidget(dialog)
    return dialog


class TestCreateMerchandiseDialog:
    def test_initial_state(self, create_customer_dialog):
        # todo: other translations
        assert_that(create_customer_dialog.windowTitle(), is_("Create customer"))

        model = create_customer_dialog.line_edit_company_name.completer().completionModel()
        assert_that(model.data(model.index(0, 0), Qt.DisplayRole), is_("company"))
        model = create_customer_dialog.line_edit_address.completer().completionModel()
        assert_that(model.data(model.index(0, 0), Qt.DisplayRole), is_("address"))

        assert_that(create_customer_dialog.line_edit_title.text(), is_(empty()))
        assert_that(create_customer_dialog.line_edit_first_name.text(), is_(empty()))
        assert_that(create_customer_dialog.line_edit_last_name.text(), is_(empty()))
        assert_that(create_customer_dialog.line_edit_company_name.text(), is_(empty()))
        assert_that(create_customer_dialog.line_edit_address.text(), is_(empty()))

    @pytest.mark.parametrize("prefix, expected_completion_count", [
        pytest.param("a", 1),
        pytest.param("add", 1),
        pytest.param("addres", 1),
        pytest.param("address", 1),
        pytest.param("x", 0),
        pytest.param("res", 0),
    ])
    def test_completion_address(self, create_customer_dialog, prefix, expected_completion_count):
        create_customer_dialog.line_edit_address.insert(prefix)
        completer = create_customer_dialog.line_edit_address.completer()

        assert_that(completer.completionPrefix(), is_(prefix))
        assert_that(completer.completionCount(), is_(expected_completion_count))
        if expected_completion_count == 1:
            completer.setCurrentRow(1)
            assert_that(completer.currentCompletion(), is_("address"))

    @pytest.mark.parametrize("button_id, slot_name", [
        pytest.param(QDialogButtonBox.Save, "save"),
        pytest.param(QDialogButtonBox.Close, "reject"),
        pytest.param(QDialogButtonBox.Reset, "reset")
    ])
    def test_slot_triggered(self, mocker, qtbot, create_customer_dialog, button_id, slot_name):
        slot = mocker.patch.object(create_customer_dialog, slot_name, autospec=True)
        button = create_customer_dialog.button_box.button(button_id)

        with qtbot.wait_signal(button.clicked):
            qtbot.mouseClick(button, Qt.LeftButton)
        slot.assert_called_once_with()

    def test_save(self, mocker, create_customer_dialog):
        title = "sample title"
        first_name = "sample first name"
        last_name = "sample last name"
        company_name = "sample company name"
        address = "sample address"

        create_customer_dialog.line_edit_title.insert(title)
        create_customer_dialog.line_edit_first_name.insert(first_name)
        create_customer_dialog.line_edit_last_name.insert(last_name)
        create_customer_dialog.line_edit_company_name.insert(company_name)
        create_customer_dialog.line_edit_address.insert(address)

        message = mocker.patch("src.customer.QtWidgets.QMessageBox.information", autospec=True)
        create_method = mocker.patch("src.customer.create_customer", autospec=True)
        create_customer_dialog.save()

        create_method.assert_called_once_with(title, first_name, last_name, company_name, address)
        message.assert_called_once_with(create_customer_dialog, "Success", f"Created new customer.")

    def test_reset(self, create_customer_dialog):
        create_customer_dialog.line_edit_title.insert("sample title")
        create_customer_dialog.line_edit_first_name.insert("sample first name")
        create_customer_dialog.line_edit_last_name.insert("sample last name")
        create_customer_dialog.line_edit_company_name.insert("sample company name")
        create_customer_dialog.line_edit_address.insert("sample address")

        create_customer_dialog.reset()

        assert_that(create_customer_dialog.line_edit_title.text(), is_(empty()))
        assert_that(create_customer_dialog.line_edit_first_name.text(), is_(empty()))
        assert_that(create_customer_dialog.line_edit_last_name.text(), is_(empty()))
        assert_that(create_customer_dialog.line_edit_company_name.text(), is_(empty()))
        assert_that(create_customer_dialog.line_edit_address.text(), is_(empty()))
