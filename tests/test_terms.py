from hamcrest import assert_that, is_
from PySide2.QtCore import Qt, QModelIndex

from src.terms import TermItem, TermType, TermModel

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
