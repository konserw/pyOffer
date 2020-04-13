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
from decimal import Decimal

import pytest
from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QModelIndex, QAbstractItemModel, QPoint, QSize
from PySide2.QtGui import QColor
from PySide2.QtSql import QSqlField, QSqlRecord
from hamcrest import assert_that, is_, greater_than, instance_of, none, empty
from qtmatchers import has_item_flags

from src.database import get_merchandise_sql_model
from src.merchandise import Merchandise, MerchandiseListModel, MerchandiseSelectionModel, MerchandiseListDelegate, \
    MerchandiseListView, MerchandiseSelectionDelegate, MerchandiseSelectionDialog, DiscountDialog


def create_merch(merchandise_id=1, list_price=9.99, count=1, discount=10):
    m = Merchandise(merchandise_id)
    m.code = "CODE"
    m.description = "DESCR"
    m.list_price = list_price
    m.count = count
    m.discount = discount
    return m


@pytest.fixture
def sample_merch():
    m = Merchandise(1)
    m.code = "CODE"
    m.description = "DESCR"
    return m


class TestMerchandise:
    def test_defaults(self, sample_merch):
        assert_that(sample_merch.list_price, is_(None))
        sample_merch.list_price = 0
        assert_that(sample_merch.discount, is_(0))
        assert_that(sample_merch.count, is_(0))
        assert_that(sample_merch.by_meter, is_(False))
        # todo other translations
        assert_that(sample_merch.unit, is_("pc."))
        assert_that(sample_merch.price, is_(0))
        assert_that(sample_merch.total, is_(0))

    @pytest.mark.parametrize("list_price, count, discount, price, total", [
        pytest.param(100, 1, 0, "100", "100"),
        pytest.param(100, 1, 10, "90", "90"),
        pytest.param(100, 2, 10, "90", "180"),
        pytest.param(99, 1, 10, "89.1", "89.1"),
        pytest.param(99, 1, 23, "76.23", "76.23"),
        pytest.param(9.99, 1, 1, "9.89", "9.89"),
        pytest.param(9.99, 10000, 1, "9.89", "98900"),
        pytest.param(1.11, 1, 10, "1", "1"),
        pytest.param(1.11, 100, 10, "1", "100"),
        pytest.param(1.11, 9, 90, "0.11", "0.99"),
    ])
    def test_total(self, list_price, count, discount, price, total):
        m = create_merch(
            list_price=list_price,
            count=count,
            discount=discount
        )
        assert_that(m.price, is_(Decimal(price)))
        assert_that(m.total, is_(Decimal(total)))

    def test_get_item(self):
        sample_merch = create_merch()
        assert_that(sample_merch[0], is_(sample_merch.code))
        assert_that(sample_merch[1], is_(sample_merch.description))
        assert_that(sample_merch[2], is_(sample_merch.list_price))
        assert_that(sample_merch[3], is_(sample_merch.discount))
        assert_that(sample_merch[4], is_(sample_merch.price))
        assert_that(sample_merch[5], is_(sample_merch.count))
        assert_that(sample_merch[6], is_(sample_merch.unit))
        assert_that(sample_merch[7], is_(sample_merch.total))

    def test_set_item(self, sample_merch):
        sample_merch[3] = 10
        assert_that(sample_merch.discount, is_(10))
        sample_merch[5] = 1
        assert_that(sample_merch.count, is_(1))

    @pytest.mark.parametrize("i", [
        pytest.param(0),
        pytest.param(1),
        pytest.param(2),
        pytest.param(4),
        pytest.param(6),
        pytest.param(7),
        pytest.param(8),
    ])
    def test_set_item_rises(self, sample_merch, i):
        with pytest.raises(RuntimeError, match="unexpected assignment"):
            sample_merch[i] = 1

    def test_eq(self, sample_merch):
        other = create_merch(1)
        assert_that(sample_merch == other, is_(True))

    def test_not_eq(self, sample_merch):
        other = create_merch(2)
        assert_that(sample_merch == other, is_(False))

    def test_unit(self, sample_merch):
        # todo: other trans
        item = create_merch()
        assert_that(item.unit, is_("pc."))
        item.by_meter = True
        assert_that(item.unit, is_("m"))


@pytest.fixture
def sample_model():
    model = MerchandiseListModel()
    model.add_item(create_merch(discount=0))
    return model


class TestMerchandiseListModel:
    # todo: other translaitons
    @pytest.mark.parametrize("i, expected", [
        pytest.param(0, "Code"),
        pytest.param(1, "Description"),
        pytest.param(2, "List Price"),
        pytest.param(3, "Discount"),
        pytest.param(4, "Price"),
        pytest.param(5, "Count"),
        pytest.param(6, "Unit"),
        pytest.param(7, "Total"),
    ])
    def test_hroizontal_header_data(self, i, expected):
        m = MerchandiseListModel()
        assert_that(m.headerData(i, Qt.Horizontal, Qt.DisplayRole))

    def test_vartical_header_data(self, sample_model):
        assert_that(sample_model.headerData(0, Qt.Vertical, Qt.DisplayRole), is_("1"))
        assert_that(sample_model.headerData(1, Qt.Vertical, Qt.DisplayRole), is_(""))

    def test_initial_row_count(self):
        m = MerchandiseListModel()
        assert_that(m.rowCount(), is_(1))

    def test_row_count(self, sample_model):
        assert_that(sample_model.rowCount(), is_(2))

    def test_column_count(self):
        m = MerchandiseListModel()
        assert_that(m.columnCount(), is_(8))

    @pytest.mark.parametrize("col, initial_value", [
        pytest.param(3, 0),
        pytest.param(5, 1),
    ])
    def test_set_data(self, sample_model, col, initial_value):
        value = 50
        assert_that(sample_model.list[0][col], is_(initial_value))
        sample_model.setData(sample_model.index(0, col), value, Qt.EditRole)
        assert_that(sample_model.list[0][col], is_(value))

    def test_data_display_role(self, sample_model):
        for key, val in enumerate(("CODE", "DESCR", "9.99", "0.0", "9.99", "1", "pc.", "9.99")):
            assert_that(sample_model.data(sample_model.index(0, key), Qt.DisplayRole), is_(val))

    def test_data_edit_role(self, sample_model):
        assert_that(sample_model.data(sample_model.index(0, 3), Qt.EditRole), is_(0))
        assert_that(sample_model.data(sample_model.index(0, 5), Qt.EditRole), is_(1))

    def test_data_alignment_role(self, sample_model):
        for key, val in enumerate((Qt.AlignLeft, Qt.AlignLeft, Qt.AlignRight, Qt.AlignRight, Qt.AlignRight, Qt.AlignRight, Qt.AlignRight, Qt.AlignRight)):
            assert_that(sample_model.data(sample_model.index(0, key), Qt.TextAlignmentRole), is_(val))

    def test_grand_total(self, sample_model):
        assert_that(sample_model.grand_total, is_(Decimal("9.99")))
        m = create_merch(count=10)
        sample_model.add_item(m)
        assert_that(sample_model.grand_total, is_(Decimal("99.89")))

    def test_supported_drop_action(self):
        m = MerchandiseListModel()
        assert_that(m.supportedDropActions(), is_(Qt.MoveAction))

    @pytest.mark.parametrize("col, expected", [
        pytest.param(0, Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable),
        pytest.param(1, Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable),
        pytest.param(2, Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable),
        pytest.param(3, Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable),
        pytest.param(4, Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable),
        pytest.param(5, Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable),
        pytest.param(6, Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable),
        pytest.param(7, Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable),
        pytest.param(8, Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable),
    ])
    def test_normal_flags(self, sample_model, col: int, expected: Qt.ItemFlags):
        assert_that(sample_model.flags(sample_model.index(0, col)), has_item_flags(expected))

    @pytest.mark.parametrize("col", [
        pytest.param(0),
        pytest.param(1),
        pytest.param(2),
        pytest.param(3),
        pytest.param(4),
        pytest.param(5),
        pytest.param(6),
        pytest.param(7),
        pytest.param(8),
    ])
    def test_last_row_flags(self, sample_model, col):
        assert_that(sample_model.flags(sample_model.index(1, col)), has_item_flags(Qt.ItemIsEnabled | Qt.ItemIsDropEnabled))

    @pytest.mark.parametrize("col", [
        pytest.param(0),
        pytest.param(1),
        pytest.param(2),
        pytest.param(3),
        pytest.param(4),
        pytest.param(5),
        pytest.param(6),
        pytest.param(7),
        pytest.param(8),
    ])
    def test_only_row_flags(self, col):
        empty_model = MerchandiseListModel()
        assert_that(empty_model.flags(empty_model.index(0, col)), has_item_flags(Qt.ItemIsEnabled | Qt.ItemIsDropEnabled))

    def test_clear(self, sample_model):
        assert_that(len(sample_model.list), is_(greater_than(0)))
        sample_model.clear()
        assert_that(len(sample_model.list), is_(0))
        sample_model.clear()
        assert_that(len(sample_model.list), is_(0))

    def test_change_item_count_same(self, sample_model):
        assert_that(len(sample_model.list), is_(1))
        assert_that(sample_model.list[0].count, is_(1))

        sample_model.change_item_count(create_merch(1, count=5))
        assert_that(len(sample_model.list), is_(1))
        assert_that(sample_model.list[0].count, is_(6))

    def test_change_item_count_different(self, sample_model):
        assert_that(len(sample_model.list), is_(1))
        assert_that(sample_model.list[0].count, is_(1))

        sample_model.change_item_count(create_merch(2, count=5))
        assert_that(len(sample_model.list), is_(2))
        assert_that(sample_model.list[0].count, is_(1))
        assert_that(sample_model.list[1].id, is_(2))
        assert_that(sample_model.list[1].count, is_(5))

    def test_remove_rows(self, sample_model):
        assert_that(len(sample_model.list), is_(1))
        assert_that(sample_model.rowCount(), is_(2))
        sample_model.removeRows(0, 1)
        assert_that(len(sample_model.list), is_(0))
        assert_that(sample_model.rowCount(), is_(1))

    def test_move_rows_0(self, sample_model):
        sample_model.add_item(create_merch(2))
        assert_that(sample_model.list[0].id, is_(1))
        assert_that(sample_model.list[1].id, is_(2))

        moved = sample_model.moveRows(QModelIndex(), 0, 1, QModelIndex(), 0)

        assert_that(moved, is_(False))
        assert_that(sample_model.list[0].id, is_(1))
        assert_that(sample_model.list[1].id, is_(2))

    def test_move_rows_1(self, sample_model):
        sample_model.add_item(create_merch(2))
        assert_that(sample_model.list[0].id, is_(1))
        assert_that(sample_model.list[1].id, is_(2))

        moved = sample_model.moveRows(QModelIndex(), 0, 1, QModelIndex(), 1)

        assert_that(moved, is_(False))
        assert_that(sample_model.list[0].id, is_(1))
        assert_that(sample_model.list[1].id, is_(2))

    def test_move_rows_2(self, sample_model):
        sample_model.add_item(create_merch(2))
        assert_that(sample_model.list[0].id, is_(1))
        assert_that(sample_model.list[1].id, is_(2))

        moved = sample_model.moveRows(QModelIndex(), 0, 1, QModelIndex(), 2)

        assert_that(moved, is_(True))
        assert_that(sample_model.list[0].id, is_(2))
        assert_that(sample_model.list[1].id, is_(1))

    def test_last_row(self, sample_model):
        # todo: other translations
        assert_that(sample_model.data(sample_model.index(1, 6), Qt.DisplayRole), is_("Total:"))
        assert_that(sample_model.data(sample_model.index(1, 7), Qt.DisplayRole), is_("9.99"))
        sample_model.add_item(create_merch(2))
        assert_that(sample_model.data(sample_model.index(2, 6), Qt.DisplayRole), is_("Total:"))
        assert_that(sample_model.data(sample_model.index(2, 7), Qt.DisplayRole), is_("18.98"))

    @pytest.mark.parametrize("ex, which", [
        pytest.param("", "both"),
        pytest.param("O", "both"),
        pytest.param("R", "second"),
        pytest.param("CODE", "first"),
        pytest.param("DESCR", "none"),
        pytest.param("S", "none"),
        pytest.param("one", "none"),
        pytest.param("E", "both"),
        pytest.param("D", "first"),
        pytest.param("Other", "second"),
        pytest.param("otheR", "second"),
        pytest.param("the", "second"),
    ])
    def test_set_discount(self, sample_model, ex, which):
        other = create_merch(2, discount=0)
        other.code = "Other"
        other.description = "otheR one"
        sample_model.add_item(other)
        assert_that(sample_model.list[0].discount, is_(0))
        assert_that(sample_model.list[1].discount, is_(0))

        discount = 50
        sample_model.set_discount(ex, discount)

        if which in ("both", "first"):
            assert_that(sample_model.list[0].discount, is_(50))
        else:
            assert_that(sample_model.list[0].discount, is_(0))
        if which in ("both", "second"):
            assert_that(sample_model.list[1].discount, is_(50))
        else:
            assert_that(sample_model.list[1].discount, is_(0))

    @pytest.mark.parametrize("ex, which", [
        pytest.param("", "both"),
        pytest.param("O", "both"),
        pytest.param("R", "second"),
        pytest.param("CODE", "first"),
        pytest.param("DESCR", "none"),
        pytest.param("S", "none"),
        pytest.param("one", "none"),
        pytest.param("E", "both"),
        pytest.param("D", "first"),
        pytest.param("Other", "second"),
        pytest.param("otheR", "second"),
        pytest.param("the", "second"),
    ])
    def test_highlight_rows(self, sample_model, ex, which):
        other = create_merch(2, discount=0)
        other.code = "Other"
        other.description = "otheR one"
        sample_model.add_item(other)
        indexes = [
            sample_model.index(0, 0),
            sample_model.index(1, 0),
        ]
        assert_that(sample_model.data(indexes[0], Qt.BackgroundRole), is_(none()))
        assert_that(sample_model.data(indexes[1], Qt.BackgroundRole), is_(none()))

        sample_model.highlight_rows(ex)

        if which in ("both", "first"):
            assert_that(sample_model.data(indexes[0], Qt.BackgroundRole), is_(QColor(0xFC, 0xF7, 0xBB)))
        else:
            assert_that(sample_model.data(indexes[0], Qt.BackgroundRole), is_(none()))
        if which in ("both", "second"):
            assert_that(sample_model.data(indexes[1], Qt.BackgroundRole), is_(QColor(0xFC, 0xF7, 0xBB)))
        else:
            assert_that(sample_model.data(indexes[1], Qt.BackgroundRole), is_(none()))

    def test_with_modeltester(self, qtmodeltester, sample_model):
        qtmodeltester.check(sample_model)


class TestMerchandiseListDelegate:
    def test_create_editor_for_discount(self, qtbot, sample_model):
        delegate = MerchandiseListDelegate(sample_model)
        widget = QtWidgets.QWidget()
        qtbot.addWidget(widget)
        editor = delegate.createEditor(widget, None, sample_model.index(0, 3))

        assert_that(editor, is_(instance_of(QtWidgets.QDoubleSpinBox)))
        assert_that(editor.decimals(), is_(1))
        assert_that(editor.minimum(), is_(0))
        assert_that(editor.singleStep(), is_(5))
        assert_that(editor.maximum(), is_(100))

    def test_create_editor_for_count(self, qtbot, sample_model):
        delegate = MerchandiseListDelegate(sample_model)
        widget = QtWidgets.QWidget()
        qtbot.addWidget(widget)
        editor = delegate.createEditor(widget, None, sample_model.index(0, 5))

        assert_that(editor, is_(instance_of(QtWidgets.QSpinBox)))
        assert_that(editor.minimum(), is_(1))
        assert_that(editor.singleStep(), is_(1))
        assert_that(editor.maximum(), is_(999999))

    @pytest.mark.parametrize("col, base", [
        pytest.param(3, 0),  # discount
        pytest.param(5, 1),  # count
    ])
    def test_update_data(self, qtbot, sample_model, col, base):
        delegate = MerchandiseListDelegate(sample_model)
        widget = QtWidgets.QWidget()
        qtbot.addWidget(widget)
        index = sample_model.index(0, col)
        editor = delegate.createEditor(widget, None, index)
        assert_that(sample_model.data(index, Qt.EditRole), is_(base))

        delegate.setEditorData(editor, index)
        assert_that(editor.value(), is_(base))

        editor.setValue(50)
        delegate.setModelData(editor, sample_model, index)
        assert_that(sample_model.data(index, Qt.DisplayRole), is_("50.0" if col == 3 else "50"))


@pytest.mark.xfail  # Events are not processed correctly in QTest
class TestMerchandiseListView:
    def test_drag_and_drop(self, qtbot, sample_model):
        sample_model.add_item(create_merch(2))
        view = MerchandiseListView()
        qtbot.addWidget(view)
        view.setModel(sample_model)
        pos0 = QPoint(view.columnViewportPosition(1), view.rowViewportPosition(0))
        assert_that(view.indexAt(pos0).data(Qt.UserRole), is_(1))
        pos1 = QPoint(view.columnViewportPosition(1), view.rowViewportPosition(1))
        assert_that(view.indexAt(pos1).data(Qt.UserRole), is_(2))
        pos2 = QPoint(view.columnViewportPosition(1), view.rowViewportPosition(2))

        qtbot.mousePress(view, Qt.LeftButton, pos=pos0)
        qtbot.mouseMove(view, pos2)
        qtbot.mouseRelease(view, Qt.LeftButton, delay=15)

        assert_that(view.indexAt(pos0).data(Qt.UserRole), is_(2))
        assert_that(view.indexAt(pos1).data(Qt.UserRole), is_(1))


class MockSourceModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_all = [
            create_merch(1, count=0, discount=0),
            create_merch(2, count=0, discount=0)
        ]
        self.list = self.list_all

    def _value(self, row, col):
        item = self.list[row]
        if col == 0:
            return item.id
        if col == 1:
            return item.code
        if col == 2:
            return item.description
        if col == 3:
            return item.unit
        if col == 4:
            return item.list_price

    def data(self, index: QModelIndex, role: int):
        return self._value(index.row(), index.column())

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.list)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 8

    def record(self, row):
        names = ("merchandise_id", "code", "description", "unit", "list_price")
        rec = QSqlRecord()
        for i, name in enumerate(names):
            f = QSqlField(name)
            f.setValue(self._value(row, i))
            rec.append(f)
        return rec


@pytest.fixture
def selection_model():
    source = MockSourceModel()
    selection = MerchandiseSelectionModel()
    selection.setSourceModel(source)
    return selection


class TestMerchandiseSelectionModel:
    def test_header_data(self, selection_model):
        assert_that(selection_model.headerData(0, Qt.Vertical), is_(None))
        # todo: other translations
        assert_that(selection_model.headerData(0, Qt.Horizontal, Qt.DisplayRole), is_("Count"))
        assert_that(selection_model.headerData(1, Qt.Horizontal, Qt.DisplayRole), is_("Code"))
        assert_that(selection_model.headerData(2, Qt.Horizontal, Qt.DisplayRole), is_("Description"))
        assert_that(selection_model.headerData(3, Qt.Horizontal, Qt.DisplayRole), is_("Unit"))
        assert_that(selection_model.headerData(4, Qt.Horizontal, Qt.DisplayRole), is_("List price"))

    def test_data(self, selection_model):
        assert_that(selection_model.data(selection_model.index(0, 0, QModelIndex()), Qt.DisplayRole), is_(0))
        assert_that(selection_model.data(selection_model.index(0, 1, QModelIndex()), Qt.DisplayRole), is_("CODE"))
        assert_that(selection_model.data(selection_model.index(0, 2, QModelIndex()), Qt.DisplayRole), is_("DESCR"))
        assert_that(selection_model.data(selection_model.index(0, 3, QModelIndex()), Qt.DisplayRole), is_("pc."))
        assert_that(selection_model.data(selection_model.index(0, 4, QModelIndex()), Qt.DisplayRole), is_(Decimal("9.99")))

    def test_row_count(self, selection_model):
        assert_that(selection_model.rowCount(), is_(2))

    def test_column_count(self, selection_model):
        assert_that(selection_model.columnCount(), is_(5))

    @pytest.mark.parametrize("col, expected", [
        pytest.param(0, Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable),
        pytest.param(1, Qt.ItemIsEnabled),
        pytest.param(2, Qt.ItemIsEnabled),
        pytest.param(3, Qt.ItemIsEnabled),
        pytest.param(4, Qt.ItemIsEnabled),
    ])
    def test_flags(self, selection_model, col, expected):
        assert_that(selection_model.flags(selection_model.index(0, col)), has_item_flags(expected))

    @pytest.mark.parametrize("loops", [
        pytest.param(1),
        pytest.param(3),
        pytest.param(5),
    ])
    def test_set_data(self, selection_model, loops):
        assert_that(selection_model.selected, is_({}))
        for i in range(1, loops+1):
            selection_model.setData(selection_model.index(0, 0), i, Qt.EditRole)
            assert_that(selection_model.selected, is_({1: create_merch(1, count=i)}))


class TestMerchandiseSelectionDelegate:
    def test_create_editor(self, qtbot, selection_model):
        delegate = MerchandiseSelectionDelegate(selection_model)
        widget = QtWidgets.QWidget()
        qtbot.addWidget(widget)
        editor = delegate.createEditor(widget, QtWidgets.QStyleOptionViewItem(), selection_model.index(0, 0))

        assert_that(editor, is_(instance_of(QtWidgets.QSpinBox)))
        assert_that(editor.minimum(), is_(0))
        assert_that(editor.singleStep(), is_(1))
        assert_that(editor.maximum(), is_(999999))

    def test_update_data(self, qtbot, selection_model):
        delegate = MerchandiseSelectionDelegate(selection_model)
        widget = QtWidgets.QWidget()
        qtbot.addWidget(widget)
        index = selection_model.index(0, 0)
        editor = delegate.createEditor(widget, QtWidgets.QStyleOptionViewItem(), index)
        base = 0
        assert_that(selection_model.data(index, Qt.DisplayRole), is_(base))

        delegate.setEditorData(editor, index)
        assert_that(editor.value(), is_(base))

        target = 50
        editor.setValue(target)
        delegate.setModelData(editor, selection_model, index)
        assert_that(selection_model.data(index, Qt.DisplayRole), is_(target))


class TestMerchandiseSelectionDialog:
    def test_initial_state(self, qtbot, selection_model):
        dialog = MerchandiseSelectionDialog(selection_model)
        qtbot.addWidget(dialog)

        # todo: other translations
        assert_that(dialog.windowTitle(), is_("Choose merchandise"))
        assert_that(dialog.size(), is_(QSize(800, 500)))
        assert_that(dialog.label.text(), is_("Filter"))
        assert_that(dialog.push_button_close.text(), is_("Add"))
        assert_that(dialog.line_edit.text(), is_(""))

    @pytest.mark.parametrize("loops", [
        pytest.param(1),
        pytest.param(3),
        pytest.param(5),
    ])
    def test_selected(self, qtbot, selection_model, loops):
        dialog = MerchandiseSelectionDialog(selection_model)
        qtbot.addWidget(dialog)
        assert_that(dialog.selected, is_({}))
        for i in range(1, loops + 1):
            selection_model.setData(selection_model.index(0, 0), i, Qt.EditRole)
            assert_that(dialog.selected, is_({1: create_merch(1, count=i)}))


@pytest.mark.usefixtures("db")
class TestMerchandiseSelectionDialogWithDB:
    def test_initial_state(self, qtbot):
        dialog = MerchandiseSelectionDialog.make()
        qtbot.addWidget(dialog)

        # todo: other translations
        assert_that(dialog.windowTitle(), is_("Choose merchandise"))
        assert_that(dialog.size(), is_(QSize(800, 500)))
        assert_that(dialog.label.text(), is_("Filter"))
        assert_that(dialog.push_button_close.text(), is_("Add"))
        assert_that(dialog.line_edit.text(), is_(""))

    @pytest.mark.parametrize("loops", [
        pytest.param(1),
        pytest.param(3),
        pytest.param(5),
    ])
    def test_selected(self, qtbot, loops):
        dialog = MerchandiseSelectionDialog.make()
        qtbot.addWidget(dialog)
        assert_that(dialog.selected, is_({}))
        for i in range(1, loops + 1):
            dialog.model.setData(dialog.model.index(0, 0), i, Qt.EditRole)
            assert_that(dialog.selected, is_({1: create_merch(1, count=i)}))


@pytest.fixture
def selection_model_with_db():
    source = get_merchandise_sql_model()
    selection = MerchandiseSelectionModel()
    selection.setSourceModel(source)
    return selection


@pytest.mark.usefixtures("db")
class TestMerchandiseSelectionModelWithDB:
    def test_header_data(self, selection_model_with_db):
        assert_that(selection_model_with_db.headerData(0, Qt.Vertical), is_(None))
        # todo: other translations
        assert_that(selection_model_with_db.headerData(0, Qt.Horizontal, Qt.DisplayRole), is_("Count"))
        assert_that(selection_model_with_db.headerData(1, Qt.Horizontal, Qt.DisplayRole), is_("Code"))
        assert_that(selection_model_with_db.headerData(2, Qt.Horizontal, Qt.DisplayRole), is_("Description"))
        assert_that(selection_model_with_db.headerData(3, Qt.Horizontal, Qt.DisplayRole), is_("Unit"))
        assert_that(selection_model_with_db.headerData(4, Qt.Horizontal, Qt.DisplayRole), is_("List price"))

    def test_data_1(self, selection_model_with_db):
        assert_that(selection_model_with_db.data(selection_model_with_db.index(0, 0, QModelIndex()), Qt.DisplayRole), is_(0))  # count
        assert_that(selection_model_with_db.data(selection_model_with_db.index(0, 1, QModelIndex()), Qt.DisplayRole), is_("CODE123"))
        assert_that(selection_model_with_db.data(selection_model_with_db.index(0, 2, QModelIndex()), Qt.DisplayRole), is_("some description"))
        assert_that(selection_model_with_db.data(selection_model_with_db.index(0, 3, QModelIndex()), Qt.DisplayRole), is_("pc."))
        assert_that(selection_model_with_db.data(selection_model_with_db.index(0, 4, QModelIndex()), Qt.DisplayRole), is_(19.99))

    def test_data_2(self, selection_model_with_db):
        assert_that(selection_model_with_db.data(selection_model_with_db.index(1, 0, QModelIndex()), Qt.DisplayRole), is_(0))  # count
        assert_that(selection_model_with_db.data(selection_model_with_db.index(1, 1, QModelIndex()), Qt.DisplayRole), is_("CODE456"))
        assert_that(selection_model_with_db.data(selection_model_with_db.index(1, 2, QModelIndex()), Qt.DisplayRole), is_("some other description"))
        assert_that(selection_model_with_db.data(selection_model_with_db.index(1, 3, QModelIndex()), Qt.DisplayRole), is_("m"))
        assert_that(selection_model_with_db.data(selection_model_with_db.index(1, 4, QModelIndex()), Qt.DisplayRole), is_(5.49))

    def test_row_count(self, selection_model_with_db):
        assert_that(selection_model_with_db.rowCount(), is_(2))

    def test_column_count(self, selection_model_with_db):
        assert_that(selection_model_with_db.columnCount(), is_(5))

    @pytest.mark.parametrize("ex, expected", [
        pytest.param("some desc", 1),
        pytest.param("other", 1),
        pytest.param("123", 1),
        pytest.param("456", 1),
        pytest.param("", 2),
        pytest.param("CODE", 2),
        pytest.param("escr", 2),
        pytest.param("Not found", 0)
    ])
    def test_search(self, selection_model_with_db, ex, expected):
        assert_that(selection_model_with_db.rowCount(), is_(2))
        selection_model_with_db.search(ex)
        assert_that(selection_model_with_db.rowCount(), is_(expected))


@pytest.fixture
def discount_dialog(qtbot):
    dialog = DiscountDialog()
    qtbot.addWidget(dialog)
    return dialog


class TestDiscountDialog:
    def test_initial_state(self, discount_dialog):
        # todo: other translations
        assert_that(discount_dialog.windowTitle(), is_("Set discounts"))
        assert_that(discount_dialog.line_edit_expression.text(), is_(""))
        assert_that(discount_dialog.label.text(), is_(
            "Please enter regular expression\n"
            "if you want to limit discount to matching items,\n"
            "or leave empty to add discount to all items."
        ))
        assert_that(discount_dialog.spinbox_discount.minimum(), is_(0))
        assert_that(discount_dialog.spinbox_discount.singleStep(), is_(5))
        assert_that(discount_dialog.spinbox_discount.maximum(), is_(100))

    @pytest.mark.parametrize("value", [
        pytest.param(0),
        pytest.param(11),
        pytest.param(50),
        pytest.param(100),
    ])
    def test_discount_value(self, discount_dialog, value):
        discount_dialog.spinbox_discount.setValue(value)
        assert_that(discount_dialog.discount_value, is_(value))

    @pytest.mark.parametrize("ex", [
        pytest.param(""),
        pytest.param("Something"),
    ])
    def test_filter_expression(self, discount_dialog, ex, qtbot):
        assert_that(discount_dialog.filter_expression, is_(empty()))
        if ex:
            qtbot.keyClicks(discount_dialog.line_edit_expression, ex)
        assert_that(discount_dialog.filter_expression, is_(ex))
