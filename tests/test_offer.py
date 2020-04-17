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

from hamcrest import assert_that, is_, instance_of, none

from src.customer import Customer
from src.merchandise import MerchandiseListModel
from src.offer import Offer
from src.user import User


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

        expected_email = "order@company.com"
        mocker.patch("src.offer.get_company_address", return_value=("lorem", "ipsum"))
        mocker.patch("src.offer.get_var", return_value=expected_email)

        offer = Offer.create_empty(user)

        assert_that(offer.merchandise_list, is_(instance_of(MerchandiseListModel)))
        assert_that(offer.customer, is_(instance_of(Customer)))
        assert_that(offer.date, is_(expected_date))
        assert_that(offer.author, is_(user))
        assert_that(offer.symbol, is_(expected_symbol))
        assert_that(offer.company_address, is_("lorem<br />\nipsum"))
        assert_that(offer.order_email, is_(expected_email))

    @pytest.mark.parametrize("i_date, i_number, expected_text", [
        pytest.param(None, None, "W odpowiedzi na zapytanie, przedstawiamy ofertę na dostawę następujących produktów:"),
        pytest.param("30.12.2020", None, "W odpowiedzi na zapytanie z dnia 30.12.2020, przedstawiamy ofertę na dostawę następujących produktów:"),
        pytest.param(None, "123", "W odpowiedzi na zapytanie numer 123, przedstawiamy ofertę na dostawę następujących produktów:"),
        pytest.param("30.12.2020", "123", "W odpowiedzi na zapytanie numer 123 z dnia 30.12.2020, przedstawiamy ofertę na dostawę następujących produktów:"),
    ])
    def test_inquiry_text(self, mocker, i_date, i_number, expected_text):
        user = mocker.create_autospec(User, instance=True)
        offer = Offer(user)
        offer.inquiry_date = i_date
        offer.inquiry_number = i_number

        assert_that(offer.inquiry_text, is_(expected_text))
