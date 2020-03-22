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
from hamcrest import assert_that, is_, none
from PySide2.QtCore import Qt, QModelIndex

from src.terms import TermItem, TermType, TermModel, TermChooserDialogFactory

SHORT_DESCRIPTION = "short description"
LONG_DESCRIPTION = "long description"


class MockSqlRecord:
    values = {
        "id": 0,
        "shortDesc": SHORT_DESCRIPTION,
        "longDesc": LONG_DESCRIPTION
    }

    def value(self, field):
        return self.values[field]


class TestTerms:
    def test_from_record(self):
        mock = MockSqlRecord()
        term = TermItem.from_record(TermType.delivery, mock)

        assert_that(term.id, is_(0))
        assert_that(term.short_desc, is_(SHORT_DESCRIPTION))
        assert_that(term.long_desc, is_(LONG_DESCRIPTION))


class TestTermModel:
    def test_vertical_header(self):
        model = TermModel()

        assert_that(model.headerData(0, Qt.Vertical, Qt.DisplayRole), is_("0"))
        assert_that(model.headerData(1, Qt.Vertical, Qt.DisplayRole), is_("1"))
        assert_that(model.headerData(2, Qt.Vertical, Qt.DisplayRole), is_("2"))

    def test_horizontal_header(self):
        model = TermModel()

        # todo: test for different localizations
        assert_that(model.headerData(0, Qt.Horizontal, Qt.DisplayRole), is_("Id"))
        assert_that(model.headerData(1, Qt.Horizontal, Qt.DisplayRole), is_("Short description"))
        assert_that(model.headerData(2, Qt.Horizontal, Qt.DisplayRole), is_("Option text"))

    def test_column_count(self):
        model = TermModel()

        assert_that(model.columnCount(QModelIndex()), is_(3))

    def test_row_count(self):
        model = TermModel()

        assert_that(model.rowCount(QModelIndex()), is_(0))

    def test_one_item(self):
        item = TermItem()
        item.id = 0
        item.short_desc = SHORT_DESCRIPTION
        item.long_desc = LONG_DESCRIPTION
        model = TermModel()
        model.add(item)

        assert_that(model.rowCount(QModelIndex()), is_(1))
        assert_that(model.data(model.index(0, 0), Qt.DisplayRole), is_("0"))
        assert_that(model.data(model.index(0, 1), Qt.DisplayRole), is_(SHORT_DESCRIPTION))
        assert_that(model.data(model.index(0, 2), Qt.DisplayRole), is_(LONG_DESCRIPTION))


class TestTermsChhoserDialog:
    @pytest.mark.parametrize("type", [
        pytest.param(TermType.billing),
        pytest.param(TermType.delivery),
        pytest.param(TermType.delivery_date),
        pytest.param(TermType.offer)
    ])
    def test_initial_state(self, qtbot, type):
        factory = TermChooserDialogFactory()
        dialog = factory.get_terms_chooser_dialog(type)
        qtbot.addWidget(dialog)

        # todo: other translations
        expected_titles = {
            TermType.billing: "Choose billing terms",
            TermType.delivery: "Choose delivery terms",
            TermType.delivery_date: "Choose delivery date terms",
            TermType.offer: "Choose offer terms"
        }
        assert_that(dialog.windowTitle(), is_(expected_titles[type]))
        assert_that(dialog.chosen_item, is_(none()))
        assert_that(dialog.ui.plainTextEdit.toPlainText(), is_(""))

