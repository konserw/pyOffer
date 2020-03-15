import pytest
from PySide2.QtCore import Qt
from hamcrest import assert_that, is_, greater_than

from src.merchandise import Merchandise, MerchandiseListModel


def _create_merch(id=1, list_price=9.99, count=1, discount=10):
    m = Merchandise(id)
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

    def test_set_discount(self, sample_merch):
        assert_that(sample_merch.discount, is_(0))
        discount = 10
        sample_merch.set_discount(discount)
        assert_that(sample_merch.discount, is_(discount))

    @pytest.mark.parametrize("list_price, count, discount, price, total", [
        pytest.param(100, 1, 0, 100, 100),
        pytest.param(100, 1, 10, 90, 90),
        pytest.param(100, 2, 10, 90, 180),
        pytest.param(99, 1, 10, 89.1, 89.1),
        pytest.param(99, 1, 23, 76.23, 76.23),
        pytest.param(9.99, 1, 1, 9.89, 9.89),
        pytest.param(9.99, 10000, 1, 9.89, 98900),
        pytest.param(1.11, 1, 10, 1, 1),
        pytest.param(1.11, 100, 10, 1, 100),
        pytest.param(1.11, 0.9, 0, 1.11, 1),
    ])
    def test_total(self, list_price, count, discount, price, total):
        m = _create_merch(
            list_price=list_price,
            count=count,
            discount=discount
        )
        assert_that(m.price, is_(price))
        assert_that(m.total, is_(total))

    def test_get_item(self):
        sample_merch = _create_merch()
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
        other = _create_merch(1)
        assert_that(sample_merch == other, is_(True))

    def test_not_eq(self, sample_merch):
        other = _create_merch(2)
        assert_that(sample_merch == other, is_(False))


@pytest.fixture
def sample_model():
    m = Merchandise(1)
    m.code = "CODE"
    m.description = "DESCR"
    m.list_price = 9.99
    m.count = 1
    model = MerchandiseListModel()
    model.add_item(m)
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

    def test_set_discount(self, sample_model):
        assert_that(sample_model.list[0].discount, is_(0))
        sample_model.setData(sample_model.index(0, 3), 10, Qt.EditRole)
        assert_that(sample_model.list[0].discount, is_(10))

    def test_set_count(self, sample_model):
        assert_that(sample_model.list[0].count, is_(1))
        sample_model.setData(sample_model.index(0, 5), 10, Qt.EditRole)
        assert_that(sample_model.list[0].count, is_(10))

    def test_data_display_role(self, sample_model):
        for key, val in enumerate(("CODE", "DESCR", 9.99, 0, 9.99, 1, "pc.", 9.99)):
            assert_that(sample_model.data(sample_model.index(0, key), Qt.DisplayRole), is_(val))

    def test_data_edit_role(self, sample_model):
        assert_that(sample_model.data(sample_model.index(0, 3), Qt.EditRole), is_(0))
        assert_that(sample_model.data(sample_model.index(0, 5), Qt.EditRole), is_(1))

    def test_data_alignment_role(self, sample_model):
        for key, val in enumerate((Qt.AlignLeft,  Qt.AlignLeft, Qt.AlignRight, Qt.AlignRight, Qt.AlignRight, Qt.AlignRight, Qt.AlignRight, Qt.AlignRight)):
            assert_that(sample_model.data(sample_model.index(0, key), Qt.TextAlignmentRole), is_(val))

    def test_grand_total(self, sample_model):
        assert_that(sample_model.grand_total, is_(9.99))
        m = _create_merch(count=10)
        sample_model.add_item(m)
        assert_that(sample_model.grand_total, is_(99.89))

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
    def test_normal_flags(self, sample_model, col, expected):
        assert_that(sample_model.flags(sample_model.index(0, col)), is_(expected))

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
        assert_that(sample_model.flags(sample_model.index(1, col)), is_(Qt.ItemIsEnabled | Qt.ItemIsDropEnabled))

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
        assert_that(empty_model.flags(empty_model.index(0, col)), is_(Qt.ItemIsEnabled | Qt.ItemIsDropEnabled))

    def test_clear(self, sample_model):
        assert_that(len(sample_model.list), is_(greater_than(0)))
        sample_model.clear()
        assert_that(len(sample_model.list), is_(0))

    def test_change_item_count_same(self, sample_model):
        assert_that(len(sample_model.list), is_(1))
        assert_that(sample_model.list[0].count, is_(1))

        sample_model.change_item_count(1, 5)
        assert_that(len(sample_model.list), is_(1))
        assert_that(sample_model.list[0].count, is_(6))
