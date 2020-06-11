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
from datetime import date

from hamcrest import assert_that, is_, instance_of, none, equal_to_ignoring_whitespace, contains_string

from src.customer import Customer
from src.merchandise import MerchandiseListModel
from src.offer import Offer
from src.user import User
from tests.test_merchandise import create_merch
from src.terms import TermItem, TermType

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
        assert_that(offer.symbol, is_(none()))
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
            <td width=40><b>Lp.</b></td>
            <td width=295><b>Towar</b></td>
            <td width=90 align=right><b>Cena kat.</b></td>
            <td width=70 align=right><b>Rabat</b></td>
            <td width=90 align=right><b>Cena</b></td>
            <td width=70 align=right><b>Ilość</b></td>
            <td width=90 align=right><b>Wartość</b></td>
        </tr></thead>

        <tr class="row1">
            <td>1</td>
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
