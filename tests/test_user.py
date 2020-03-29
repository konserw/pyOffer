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
from datetime import date

import pytest
from hamcrest import assert_that, is_
from mock import patch

from src.user import User

USER_ID = 1
NAME = "name"
MAIL = "name@company.com"
MALE = False
PHONE = "555 55 55"
CHAR_FOR_OFFER_SYMBOL = "N"
BUSINESS_SYMBOL = "X"


class FakeRecord:
    def __init__(self):
        self.dict = {
            "user_id": USER_ID,
            "name": NAME,
            "mail": MAIL,
            "male": MALE,
            "phone": PHONE,
            "char_for_offer_symbol": CHAR_FOR_OFFER_SYMBOL,
            "business_symbol": BUSINESS_SYMBOL,
        }

    def value(self, key):
        return self.dict[key]


@pytest.fixture
def user():
    u = User()
    u.id = USER_ID
    u.name = NAME
    u.mail = MAIL
    u.male = MALE
    u.phone = PHONE
    u.char_for_offer_symbol = CHAR_FOR_OFFER_SYMBOL
    u.business_symbol = BUSINESS_SYMBOL
    return u


class TestUser:
    def test_user_from_record(self):
        user = User.from_sql_record(FakeRecord())

        assert_that(user.id, is_(USER_ID))
        assert_that(user.name, is_(NAME))
        assert_that(user.mail, is_(MAIL))
        assert_that(user.male, is_(MALE))
        assert_that(user.phone, is_(PHONE))
        assert_that(user.char_for_offer_symbol, is_(CHAR_FOR_OFFER_SYMBOL))
        assert_that(user.business_symbol, is_(BUSINESS_SYMBOL))

    @pytest.mark.parametrize("male, suffix", [
        pytest.param(True, ""),
        pytest.param(False, "a"),
    ])
    def test_gender_suffix(self, user, male, suffix):
        user.male = male
        assert_that(user.gender_suffix, is_(suffix))

    def test_new_offer_symbol(self, monkeypatch, user):
        with patch("src.user.date") as mock_date:
            mock_date.today.return_value = date(2020, 12, 15)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

            monkeypatch.setattr("src.user.get_new_offer_number", lambda _: 8)

            assert_that(user.new_offer_symbol(), is_("X2012N08"))
