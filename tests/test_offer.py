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
from hamcrest import assert_that, is_, instance_of, equal_to_ignoring_whitespace, contains_string, not_

from src.customer import Customer
from src.merchandise import MerchandiseListModel
from src.offer import Offer, PrintOptions
from src.terms import TermItem, TermType
from src.user import User
from tests.test_merchandise import create_merch

remarks_test_set = [
    pytest.param("one liner", "one liner"),
    pytest.param("two\nlines", "two<br />\nlines"),
    pytest.param("or\nthree\nlines", "or<br />\nthree<br />\nlines"),
]
terms_test_set = [
    pytest.param(TermType.delivery, "Warunki dostawy"),
    pytest.param(TermType.offer, "Warunki oferty"),
    pytest.param(TermType.billing, "Warunki płatności"),
    pytest.param(TermType.delivery_date, "Termin dostawy"),
]


class TestOffer:
    def test_new_symbol(self, mocker):
        expected_symbol = "X2012N08"
        user = mocker.create_autospec(User, instance=True)
        user.new_offer_symbol.return_value = expected_symbol

        offer = Offer(user)
        assert_that(offer.symbol, is_(""))
        offer.new_symbol()
        assert_that(offer.symbol, is_(expected_symbol))

    def test_create_empty(self, mocker):
        expected_symbol = "X2012N08"
        user = mocker.create_autospec(User, instance=True)
        user.new_offer_symbol.return_value = expected_symbol

        expected_date = date(2020, 12, 15)
        mock_date = mocker.patch("src.offer.date", autospec=True)
        mock_date.today.return_value = expected_date

        vars = {
            "order email": "order@company.com",
            "HQ": "lorem<br />ipsum"
        }
        mocker.patch("src.offer.get_var", autospce=True, side_effect=lambda key: vars[key])

        offer = Offer.create_empty(user)

        assert_that(offer.merchandise_list, is_(instance_of(MerchandiseListModel)))
        assert_that(offer.customer, is_(instance_of(Customer)))
        assert_that(offer.date, is_(expected_date))
        assert_that(offer.author, is_(user))
        assert_that(offer.symbol, is_(expected_symbol))
        assert_that(offer.company_address, is_(vars["HQ"]))
        assert_that(offer.order_email, is_(vars["order email"]))

    @pytest.mark.parametrize("i_date, i_number, expected_text", [
        pytest.param(None, None, "W odpowiedzi na zapytanie, przedstawiamy ofertę na dostawę następujących produktów:"),
        pytest.param("30.12.2020", None, "W odpowiedzi na zapytanie z dnia 30.12.2020, przedstawiamy ofertę na dostawę następujących produktów:"),
        pytest.param(None, "123", "W odpowiedzi na zapytanie numer 123, przedstawiamy ofertę na dostawę następujących produktów:"),
        pytest.param("30.12.2020", "123", "W odpowiedzi na zapytanie numer 123 z dnia 30.12.2020, przedstawiamy ofertę na dostawę następujących produktów:"),
    ])
    def test_inquiry_text(self, i_date, i_number, expected_text):
        offer = Offer()
        offer.inquiry_date = i_date
        offer.inquiry_number = i_number

        assert_that(offer.inquiry_text, is_(expected_text))

    def test_empty_terms_table(self):
        offer = Offer()

        terms_table = offer.terms_table()

        expected_terms_table = "<table cellspacing=3></table>"
        assert_that(terms_table, is_(equal_to_ignoring_whitespace(expected_terms_table)))

    @pytest.mark.parametrize("term_type, term_type_desc", terms_test_set)
    def test_terms_table(self, term_type, term_type_desc):
        text = "Some terms text"
        offer = Offer()
        offer.terms = {term_type: (TermItem(term_type, text))}

        terms_table = offer.terms_table()

        expected_terms_table = f"""
<table cellspacing=3>
    <tr>
        <td width=140>{term_type_desc}:</td>
        <td width=602>{text}</td>
    </tr>
</table>
"""
        assert_that(terms_table, is_(equal_to_ignoring_whitespace(expected_terms_table)))

    @pytest.mark.parametrize("remarks, expected_remarks", remarks_test_set)
    def test_terms_table_remarks(self, remarks, expected_remarks):
        offer = Offer()
        offer.remarks = remarks

        terms_table = offer.terms_table()

        expected_terms_table = f"""
<table cellspacing=3>
    <tr>
        <td width=140>Uwagi:</td>
        <td width=602>{expected_remarks}</td>
    </tr>
</table>
"""
        assert_that(terms_table, is_(equal_to_ignoring_whitespace(expected_terms_table)))

    @pytest.mark.parametrize("term_type, term_type_desc", terms_test_set)
    @pytest.mark.parametrize("remarks, expected_remarks", remarks_test_set)
    def test_terms_table_with_remarks(self, term_type, term_type_desc, remarks, expected_remarks):
        text = "Some terms text"
        offer = Offer()
        offer.remarks = remarks
        offer.terms = {term_type: (TermItem(term_type, text))}

        terms_table = offer.terms_table()

        expected_terms_table = f"""
<table cellspacing=3>
    <tr>
        <td width=140>{term_type_desc}:</td>
        <td width=602>{text}</td>
    </tr>
    <tr>
        <td width=140>Uwagi:</td>
        <td width=602>{expected_remarks}</td>
    </tr>
</table>
        """
        assert_that(terms_table, is_(equal_to_ignoring_whitespace(expected_terms_table)))

    def test_full_terms_table(self):
        remarks = "some remarks"
        test_terms = [
            (TermType.delivery, "Warunki dostawy", "Some delivery terms text"),
            (TermType.offer, "Warunki oferty", "Some offer terms text"),
            (TermType.billing, "Warunki płatności", "Some billing terms text"),
            (TermType.delivery_date, "Termin dostawy", "Some delivery date terms text"),
        ]
        offer = Offer()
        offer.remarks = remarks
        offer.terms = {}
        for row in test_terms:
            term_type = row[0]
            offer.terms[term_type] = TermItem(term_type, row[2])

        terms_table = offer.terms_table()

        for row in test_terms:
            expected_terms_text = f"""
    <tr>
        <td width=140>{row[1]}:</td>
        <td width=602>{row[2]}</td>
    </tr>
"""
            assert_that(terms_table, contains_string(expected_terms_text))
        expected_remarks_text = f"""
    <tr>
        <td width=140>Uwagi:</td>
        <td width=602>{remarks}</td>
    </tr>
"""
        assert_that(terms_table, contains_string(expected_remarks_text))

    def test_empty_merchandise_table(self):
        offer = Offer()
        offer.merchandise_list = MerchandiseListModel(offer)

        merchandise_table = offer.merchanidse_table()

        expected_merchandise_table = """
    <table cellspacing=0>
        <thead><tr class="header">
            <td width=40 align=left><b>Lp.</b></td>
            <td width=295 align=left><b>Towar</b></td>
            <td width=90 align=right><b>Cena kat.</b></td>
            <td width=70 align=right><b>Rabat</b></td>
            <td width=90 align=right><b>Cena</b></td>
            <td width=70 align=right><b>Ilość</b></td>
            <td width=90 align=right><b>Wartość</b></td>
        </tr></thead>

        <tr style="font-weight:bold;">
            <td align=right colspan=6>Razem:</td>
            <td align=right>0.00 zł</td>
        </tr>
    </table>
"""
        assert_that(merchandise_table, is_(equal_to_ignoring_whitespace(expected_merchandise_table)))

    def test_merchandise_table_with_all_columns(self):
        offer = Offer()
        offer.merchandise_list = MerchandiseListModel(offer)
        offer.merchandise_list.add_item(create_merch())

        merchandise_table = offer.merchanidse_table()

        expected_merchandise_table = """
    <table cellspacing=0>
        <thead><tr class="header">
            <td width=40 align=left><b>Lp.</b></td>
            <td width=295 align=left><b>Towar</b></td>
            <td width=90 align=right><b>Cena kat.</b></td>
            <td width=70 align=right><b>Rabat</b></td>
            <td width=90 align=right><b>Cena</b></td>
            <td width=70 align=right><b>Ilość</b></td>
            <td width=90 align=right><b>Wartość</b></td>
        </tr></thead>

        <tr class="row1">
            <td align=right style="padding-right: 5">1</td>
            <td>CODE</td>
            <td align=right>9.99 zł</td>
            <td align=right>10.0%</td>
            <td align=right>8.99 zł</td>
            <td align=right>1 szt.</td>
            <td align=right>8.99 zł</td>
        </tr>
        <tr class="row1 spec">
            <td></td>
            <td colspan=6>DESCR</td>
        </tr>

        <tr style="font-weight:bold;">
            <td align=right colspan=6>Razem:</td>
            <td align=right>8.99 zł</td>
        </tr>
    </table>
"""
        assert_that(merchandise_table, is_(equal_to_ignoring_whitespace(expected_merchandise_table)))

    def test_merchandise_table_without_no(self):
        offer = Offer()
        offer.merchandise_list = MerchandiseListModel(offer)
        offer.merchandise_list.add_item(create_merch())

        merchandise_table = offer.merchanidse_table(PrintOptions(print_no=False))

        expected_merchandise_table = """
        <table cellspacing=0>
            <thead><tr class="header">
                <td width=335 align=left><b>Towar</b></td>
                <td width=90 align=right><b>Cena kat.</b></td>
                <td width=70 align=right><b>Rabat</b></td>
                <td width=90 align=right><b>Cena</b></td>
                <td width=70 align=right><b>Ilość</b></td>
                <td width=90 align=right><b>Wartość</b></td>
            </tr></thead>

            <tr class="row1">
                <td>CODE</td>
                <td align=right>9.99 zł</td>
                <td align=right>10.0%</td>
                <td align=right>8.99 zł</td>
                <td align=right>1 szt.</td>
                <td align=right>8.99 zł</td>
            </tr>
            <tr class="row1 spec">
                <td></td>
                <td colspan=5>DESCR</td>
            </tr>

            <tr style="font-weight:bold;">
                <td align=right colspan=5>Razem:</td>
                <td align=right>8.99 zł</td>
            </tr>
        </table>
    """
        assert_that(merchandise_table, is_(equal_to_ignoring_whitespace(expected_merchandise_table)))

    def test_merchandise_table_without_list_price(self):
        offer = Offer()
        offer.merchandise_list = MerchandiseListModel(offer)
        offer.merchandise_list.add_item(create_merch())

        merchandise_table = offer.merchanidse_table(PrintOptions(print_list_price=False))

        expected_merchandise_table = """
        <table cellspacing=0>
            <thead><tr class="header">
                <td width=40 align=left><b>Lp.</b></td>
                <td width=385 align=left><b>Towar</b></td>
                <td width=70 align=right><b>Rabat</b></td>
                <td width=90 align=right><b>Cena</b></td>
                <td width=70 align=right><b>Ilość</b></td>
                <td width=90 align=right><b>Wartość</b></td>
            </tr></thead>

            <tr class="row1">
                <td align=right style="padding-right: 5">1</td>
                <td>CODE</td>
                <td align=right>10.0%</td>
                <td align=right>8.99 zł</td>
                <td align=right>1 szt.</td>
                <td align=right>8.99 zł</td>
            </tr>
            <tr class="row1 spec">
                <td></td>
                <td colspan=5>DESCR</td>
            </tr>

            <tr style="font-weight:bold;">
                <td align=right colspan=5>Razem:</td>
                <td align=right>8.99 zł</td>
            </tr>
        </table>
    """
        assert_that(merchandise_table, is_(equal_to_ignoring_whitespace(expected_merchandise_table)))

    def test_merchandise_table_without_discount(self):
        offer = Offer()
        offer.merchandise_list = MerchandiseListModel(offer)
        offer.merchandise_list.add_item(create_merch())

        merchandise_table = offer.merchanidse_table(PrintOptions(print_discount=False))

        expected_merchandise_table = """
    <table cellspacing=0>
        <thead><tr class="header">
            <td width=40 align=left><b>Lp.</b></td>
            <td width=365 align=left><b>Towar</b></td>
            <td width=90 align=right><b>Cena kat.</b></td>
            <td width=90 align=right><b>Cena</b></td>
            <td width=70 align=right><b>Ilość</b></td>
            <td width=90 align=right><b>Wartość</b></td>
        </tr></thead>

        <tr class="row1">
            <td align=right style="padding-right: 5">1</td>
            <td>CODE</td>
            <td align=right>9.99 zł</td>
            <td align=right>8.99 zł</td>
            <td align=right>1 szt.</td>
            <td align=right>8.99 zł</td>
        </tr>
        <tr class="row1 spec">
            <td></td>
            <td colspan=5>DESCR</td>
        </tr>

        <tr style="font-weight:bold;">
            <td align=right colspan=5>Razem:</td>
            <td align=right>8.99 zł</td>
        </tr>
    </table>
"""
        assert_that(merchandise_table, is_(equal_to_ignoring_whitespace(expected_merchandise_table)))

    def test_merchandise_table_without_price(self):
        offer = Offer()
        offer.merchandise_list = MerchandiseListModel(offer)
        offer.merchandise_list.add_item(create_merch())

        merchandise_table = offer.merchanidse_table(PrintOptions(print_price=False))

        expected_merchandise_table = """
    <table cellspacing=0>
        <thead><tr class="header">
            <td width=40 align=left><b>Lp.</b></td>
            <td width=385 align=left><b>Towar</b></td>
            <td width=90 align=right><b>Cena kat.</b></td>
            <td width=70 align=right><b>Rabat</b></td>
            <td width=70 align=right><b>Ilość</b></td>
            <td width=90 align=right><b>Wartość</b></td>
        </tr></thead>

        <tr class="row1">
            <td align=right style="padding-right: 5">1</td>
            <td>CODE</td>
            <td align=right>9.99 zł</td>
            <td align=right>10.0%</td>
            <td align=right>1 szt.</td>
            <td align=right>8.99 zł</td>
        </tr>
        <tr class="row1 spec">
            <td></td>
            <td colspan=5>DESCR</td>
        </tr>

        <tr style="font-weight:bold;">
            <td align=right colspan=5>Razem:</td>
            <td align=right>8.99 zł</td>
        </tr>
    </table>
"""
        assert_that(merchandise_table, is_(equal_to_ignoring_whitespace(expected_merchandise_table)))

    def test_merchandise_table_without_quantity(self):
        offer = Offer()
        offer.merchandise_list = MerchandiseListModel(offer)
        offer.merchandise_list.add_item(create_merch())

        merchandise_table = offer.merchanidse_table(PrintOptions(print_quantity=False))

        expected_merchandise_table = """
    <table cellspacing=0>
        <thead><tr class="header">
            <td width=40 align=left><b>Lp.</b></td>
            <td width=365 align=left><b>Towar</b></td>
            <td width=90 align=right><b>Cena kat.</b></td>
            <td width=70 align=right><b>Rabat</b></td>
            <td width=90 align=right><b>Cena</b></td>
            <td width=90 align=right><b>Wartość</b></td>
        </tr></thead>

        <tr class="row1">
            <td align=right style="padding-right: 5">1</td>
            <td>CODE</td>
            <td align=right>9.99 zł</td>
            <td align=right>10.0%</td>
            <td align=right>8.99 zł</td>
            <td align=right>8.99 zł</td>
        </tr>
        <tr class="row1 spec">
            <td></td>
            <td colspan=5>DESCR</td>
        </tr>

        <tr style="font-weight:bold;">
            <td align=right colspan=5>Razem:</td>
            <td align=right>8.99 zł</td>
        </tr>
    </table>
"""
        assert_that(merchandise_table, is_(equal_to_ignoring_whitespace(expected_merchandise_table)))

    def test_merchandise_table_without_description(self):
        offer = Offer()
        offer.merchandise_list = MerchandiseListModel(offer)
        offer.merchandise_list.add_item(create_merch())

        merchandise_table = offer.merchanidse_table(PrintOptions(print_description=False))

        expected_merchandise_table = """
    <table cellspacing=0>
        <thead><tr class="header">
            <td width=40 align=left><b>Lp.</b></td>
            <td width=295 align=left><b>Towar</b></td>
            <td width=90 align=right><b>Cena kat.</b></td>
            <td width=70 align=right><b>Rabat</b></td>
            <td width=90 align=right><b>Cena</b></td>
            <td width=70 align=right><b>Ilość</b></td>
            <td width=90 align=right><b>Wartość</b></td>
        </tr></thead>

        <tr class="row1">
            <td align=right style="padding-right: 5">1</td>
            <td>CODE</td>
            <td align=right>9.99 zł</td>
            <td align=right>10.0%</td>
            <td align=right>8.99 zł</td>
            <td align=right>1 szt.</td>
            <td align=right>8.99 zł</td>
        </tr>

        <tr style="font-weight:bold;">
            <td align=right colspan=6>Razem:</td>
            <td align=right>8.99 zł</td>
        </tr>
    </table>
"""
        assert_that(merchandise_table, is_(equal_to_ignoring_whitespace(expected_merchandise_table)))

    def test_merchandise_table_without_list_price_and_discount(self):
        offer = Offer()
        offer.merchandise_list = MerchandiseListModel(offer)
        offer.merchandise_list.add_item(create_merch())

        merchandise_table = offer.merchanidse_table(PrintOptions(print_list_price=False, print_discount=False))

        expected_merchandise_table = """
    <table cellspacing=0>
        <thead><tr class="header">
            <td width=40 align=left><b>Lp.</b></td>
            <td width=455 align=left><b>Towar</b></td>
            <td width=90 align=right><b>Cena</b></td>
            <td width=70 align=right><b>Ilość</b></td>
            <td width=90 align=right><b>Wartość</b></td>
        </tr></thead>

        <tr class="row1">
            <td align=right style="padding-right: 5">1</td>
            <td>CODE</td>
            <td align=right>8.99 zł</td>
            <td align=right>1 szt.</td>
            <td align=right>8.99 zł</td>
        </tr>
        <tr class="row1 spec">
            <td></td>
            <td colspan=4>DESCR</td>
        </tr>

        <tr style="font-weight:bold;">
            <td align=right colspan=4>Razem:</td>
            <td align=right>8.99 zł</td>
        </tr>
    </table>
"""
        assert_that(merchandise_table, is_(equal_to_ignoring_whitespace(expected_merchandise_table)))

    def test_merchandise_table_without_price_and_quantity(self):
        offer = Offer()
        offer.merchandise_list = MerchandiseListModel(offer)
        offer.merchandise_list.add_item(create_merch())

        merchandise_table = offer.merchanidse_table(PrintOptions(print_price=False, print_quantity=False))

        expected_merchandise_table = """
    <table cellspacing=0>
        <thead><tr class="header">
            <td width=40 align=left><b>Lp.</b></td>
            <td width=455 align=left><b>Towar</b></td>
            <td width=90 align=right><b>Cena kat.</b></td>
            <td width=70 align=right><b>Rabat</b></td>
            <td width=90 align=right><b>Wartość</b></td>
        </tr></thead>

        <tr class="row1">
            <td align=right style="padding-right: 5">1</td>
            <td>CODE</td>
            <td align=right>9.99 zł</td>
            <td align=right>10.0%</td>
            <td align=right>8.99 zł</td>
        </tr>
        <tr class="row1 spec">
            <td></td>
            <td colspan=4>DESCR</td>
        </tr>

        <tr style="font-weight:bold;">
            <td align=right colspan=4>Razem:</td>
            <td align=right>8.99 zł</td>
        </tr>
    </table>
"""
        assert_that(merchandise_table, is_(equal_to_ignoring_whitespace(expected_merchandise_table)))

    def test_merchandise_table_with_minimum_subset(self):
        offer = Offer()
        offer.merchandise_list = MerchandiseListModel(offer)
        offer.merchandise_list.add_item(create_merch())

        merchandise_table = offer.merchanidse_table(PrintOptions(False, True, False, False, False, False, False, True))

        expected_merchandise_table = """
    <table cellspacing=0>
        <thead><tr class="header">
            <td width=655 align=left><b>Towar</b></td>
            <td width=90 align=right><b>Wartość</b></td>
        </tr></thead>

        <tr class="row1">
            <td>CODE</td>
            <td align=right>8.99 zł</td>
        </tr>

        <tr style="font-weight:bold;">
            <td align=right colspan=1>Razem:</td>
            <td align=right>8.99 zł</td>
        </tr>
    </table>
"""
        assert_that(merchandise_table, is_(equal_to_ignoring_whitespace(expected_merchandise_table)))

    @pytest.mark.parametrize("symbol", [
        pytest.param("X2012N08"),
        pytest.param("A2011B01"),
    ])
    def test_header_table_symbol(self, mocker, symbol):
        user = mocker.create_autospec(User(), spec_set=True)
        user.name = ""
        user.mail = ""
        user.gender_suffix = ""
        user.phone = ""

        offer = Offer(user)
        offer.date = date(2020, 12, 15)
        offer.symbol = symbol
        header_table = offer.header_table()

        expected = f"Oferta nr: <b>{symbol}</b><br />"
        assert_that(header_table, contains_string(expected))

    @pytest.mark.parametrize("offer_date, expected_date", [
        pytest.param(date(2020, 12, 15), "15.12.2020"),
        pytest.param(date(1999, 12, 15), "15.12.1999"),
        pytest.param(date(2020, 1, 15), "15.01.2020"),
        pytest.param(date(2020, 12, 1), "01.12.2020"),
        pytest.param(date(2020, 1, 1), "01.01.2020"),
    ])
    def test_header_table_date(self, mocker, offer_date, expected_date):
        user = mocker.create_autospec(User(), spec_set=True)
        user.name = ""
        user.mail = ""
        user.gender_suffix = ""
        user.phone = ""

        offer = Offer(user)
        offer.date = offer_date
        header_table = offer.header_table()

        expected = f"Z dnia: {expected_date}<br />"
        assert_that(header_table, contains_string(expected))

    @pytest.mark.parametrize("company_name, html_address, concated_name", [
        pytest.param("Some Company", "255 Some street\n<br />In some town", "Mr. John Smith"),
        pytest.param("Some Company", "255 Some street\n<br />In some town\n<br />State or something", "Mr. John Smith"),
        pytest.param("Full business name that is quite long", "255 Some street\n<br />In some town", "Mr. John Smith"),
        pytest.param("Full business name that is quite long", "255 Some street\n<br />In some town", "Ms. Jane Doe"),
    ])
    def test_header_table_customer(self, mocker, company_name, html_address, concated_name):
        user = mocker.create_autospec(User(), spec_set=True)
        user.name = ""
        user.mail = ""
        user.gender_suffix = ""
        user.phone = ""
        customer = mocker.create_autospec(Customer(), spec_set=True)
        customer.id = 1
        customer.company_name = company_name
        customer.concated_name = concated_name
        customer.html_address = html_address

        offer = Offer(user)
        offer.date = date(2020, 12, 15)
        offer.customer = customer
        header_table = offer.header_table()

        expected = f"""
            Dla:<br />
            <b>{company_name}</b><br />
            {html_address}<br />
            {concated_name}
"""
        assert_that(header_table, contains_string(expected))

    @pytest.mark.parametrize("name, mail, phone", [
        pytest.param("Mr. John Smith", "john.smith@company.com", "123 456 789"),
        pytest.param("Ms. Jane Doe", "jane.doe@company.com", "7895464312"),
    ])
    @pytest.mark.parametrize("company", [
        pytest.param("Some company"),
        pytest.param("Full business name that is quite long"),
        pytest.param("Full business name that is quite long<br />With address<br />And town"),
    ])
    def test_header_table_author(self, mocker, company, name, mail, phone):
        user = mocker.create_autospec(User(), spec_set=True)
        user.name = name
        user.mail = mail
        user.phone = phone

        offer = Offer(user)
        offer.company_address = company
        offer.date = date(2020, 12, 15)
        header_table = offer.header_table()

        expected = f"""
        <td width=315>
            {company}<br />
            <b>{name}</b><br />
            {mail}<br />
            Tel.: {phone}
        </td>
"""
        assert_that(header_table, contains_string(expected))

    @pytest.mark.parametrize("company, name, mail", [
        pytest.param("Some company", "Mr. John Smith", "john.smith@company.com"),
        pytest.param("Some company", "Ms. Jane Doe", "jane.doe@company.com"),
    ])
    def test_header_table_author_no_phone(self, mocker, company, name, mail):
        user = mocker.create_autospec(User(), spec_set=True)
        user.name = name
        user.mail = mail
        user.phone = None

        offer = Offer(user)
        offer.company_address = company
        offer.date = date(2020, 12, 15)
        header_table = offer.header_table()

        expected = f"""
        <td width=315>
            {company}<br />
            <b>{name}</b><br />
            {mail}<br />
"""
        assert_that(header_table, contains_string(expected))
        assert_that(header_table, not_(contains_string("Tel")))

    def test_full_header_table(self, mocker):
        expected_date = date(2020, 12, 15)
        mock_date = mocker.patch("src.offer.date", autospec=True)
        mock_date.today.return_value = expected_date

        vars = {
            "order email": "order@company.com",
            "HQ": "lorem<br />ipsum"
        }
        mocker.patch("src.offer.get_var", autospce=True, side_effect=lambda key: vars[key])

        expected_symbol = "X2012N08"
        user = mocker.create_autospec(User(), spec_set=True)
        user.new_offer_symbol.return_value = expected_symbol
        user.name = "Author Name"
        user.mail = "author@company.com"
        user.gender_suffix = "a"
        user.phone = "123 456 789"

        offer = Offer.create_empty(user)

        customer = mocker.create_autospec(Customer(), spec_set=True)
        customer.id = 1
        customer.company_name = "Full business name"
        customer.concated_name = "Mr John Doe"
        customer.html_address = "255 Some street<br />\nIn some town"
        offer.customer = customer

        header_table = offer.header_table()
        expected_header_table = """
    <table>
    <tr>
        <td valign=top width=315>
            Oferta nr: <b>X2012N08</b><br />
            Z dnia: 15.12.2020<br />
            Dla:<br />
            <b>Full business name</b><br />
            255 Some street<br />
In some town<br />
            Mr John Doe
        </td>
        <td width=315>
            lorem<br />ipsum<br />
            <b>Author Name</b><br />
            author@company.com<br />
            Tel.: 123 456 789
        </td>
        <td width=115 align=right>
            <img src=:/logos width=114 valign=top>
        </td>
    </tr>
    <tr>
        <td colspan=3>
            <hr width=100%>
        </td>
    </tr>
    </table>
"""
        assert_that(header_table, is_(equal_to_ignoring_whitespace(expected_header_table)))

    @pytest.mark.parametrize("suffix, name, order_mail", [
        pytest.param("", "Mr. John Smith", "office@company.com"),
        pytest.param("a", "Ms. Jane Doe", "billing@company.com"),
    ])
    def test_footer(self, mocker, suffix, name, order_mail):
        user = mocker.create_autospec(User(), spec_set=True)
        user.name = name
        user.gender_suffix = suffix

        offer = Offer(user)
        offer.order_email = order_mail
        offer.date = date(2020, 12, 15)
        header_table = offer.footer()

        expected = f"""
    <p>
    <b>Zamówienia prosimy kierować na adres:</b> {order_mail} z kopią do autora oferty.<br />
    <br />
    Łączymy pozdrowienia.
    </p>
    <p align=center style="margin-left: 500">
        Ofertę przygotował{suffix}<br /><br /><br />
        {name}
    </p>
"""
        assert_that(header_table, contains_string(expected))

    def test_whole_printout(self, mocker):
        expected_date = date(2020, 12, 15)
        mock_date = mocker.patch("src.offer.date", autospec=True)
        mock_date.today.return_value = expected_date

        vars = {
            "order email": "order@company.com",
            "HQ": "lorem<br />ipsum"
        }
        mocker.patch("src.offer.get_var", autospce=True, side_effect=lambda key: vars[key])

        expected_symbol = "X2012N08"
        user = mocker.create_autospec(User(), spec_set=True)
        user.new_offer_symbol.return_value = expected_symbol
        user.name = "Author Name"
        user.mail = "author@company.com"
        user.gender_suffix = "a"
        user.phone = "123 456 789"

        offer = Offer.create_empty(user)

        customer = mocker.create_autospec(Customer(), spec_set=True)
        customer.id = 1
        customer.company_name = "Full business name"
        customer.concated_name = "Mr John Doe"
        customer.html_address = "255 Some street<br />\nIn some town"
        offer.customer = customer

        offer.merchandise_list.add_item(create_merch())
        offer.remarks = "Some remarks"

        expected_document = """<html>
<head>
<title>Oferta</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>
<style>
    .spec { font-size: 6pt; }
    .row0 { background: #efefef; }
    .row1 { background: #dadada; }
</style>
</head>
<body>
<table>
<thead>
<tr><td>
    <table>
    <tr>
        <td valign=top width=315>
            Oferta nr: <b>X2012N08</b><br />
            Z dnia: 15.12.2020<br />
            Dla:<br />
            <b>Full business name</b><br />
            255 Some street<br />
In some town<br />
            Mr John Doe
        </td>
        <td width=315>
            lorem<br />ipsum<br />
            <b>Author Name</b><br />
            author@company.com<br />
            Tel.: 123 456 789
        </td>
        <td width=115 align=right>
            <img src=:/logos width=114 valign=top>
        </td>
    </tr>
    <tr>
        <td colspan=3>
            <hr width=100%>
        </td>
    </tr>
    </table>
</td></tr>
</thead>
<tbody>
<tr><td>
    W odpowiedzi na zapytanie, przedstawiamy ofertę na dostawę następujących produktów:
</td></tr>
<tr><td>
    
    <table cellspacing=0>
        <thead><tr class="header">
            <td width=40 align=left><b>Lp.</b></td>
            <td width=295 align=left><b>Towar</b></td>
            <td width=90 align=right><b>Cena kat.</b></td>
            <td width=70 align=right><b>Rabat</b></td>
            <td width=90 align=right><b>Cena</b></td>
            <td width=70 align=right><b>Ilość</b></td>
            <td width=90 align=right><b>Wartość</b></td>
        </tr></thead>

        <tr class="row1">
            <td align=right style="padding-right: 5">1</td>
            <td>CODE</td>
            <td align=right>9.99 zł</td>
            <td align=right>10.0%</td>
            <td align=right>8.99 zł</td>
            <td align=right>1 szt.</td>
            <td align=right>8.99 zł</td>
        </tr>
        <tr class="row1 spec">
            <td></td>
            <td colspan=6>DESCR</td>
        </tr>

        <tr style="font-weight:bold;">
            <td align=right colspan=6>Razem:</td>
            <td align=right>8.99 zł</td>
        </tr>
    </table>

</td></tr>
<tr><td>
    Podane ceny nie zawierają podatku VAT<br />
</td></tr>
<tr><td>
<table cellspacing=3>
    <tr>
        <td width=140>Uwagi:</td>
        <td width=602>Some remarks</td>
    </tr>
</table>

</td></tr>
<tr><td>
    <p>
    <b>Zamówienia prosimy kierować na adres:</b> order@company.com z kopią do autora oferty.<br />
    <br />
    Łączymy pozdrowienia.
    </p>
    <p align=center style="margin-left: 500">
        Ofertę przygotowała<br /><br /><br />
        Author Name
    </p>
</td></tr>
</tbody>
</table>
</body>
</html>
"""

        document = offer.printout()
        assert_that(document, is_(equal_to_ignoring_whitespace(expected_document)))
