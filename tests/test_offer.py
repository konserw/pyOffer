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

        offer = Offer.create_empty(user)

        assert_that(offer.merchandise_list, is_(instance_of(MerchandiseListModel)))
        assert_that(offer.customer, is_(instance_of(Customer)))
        assert_that(offer.date, is_(expected_date))
        assert_that(offer.author, is_(user))
        assert_that(offer.symbol, is_(expected_symbol))
