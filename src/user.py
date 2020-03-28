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


class User:
    def __init__(self):
        self.id = None
        self.name = None
        self.phone = None
        self.mail = None
        self.male = True
        self.char_for_offer_symbol = None
        self.business_symbol = None

    def get_gender_suffix(self):
        if not self.male:
            return "a"
        return ""

    @staticmethod
    def from_sql_record(rec):
        user = User()
        user.name = rec.field("name").value
        user.phone = rec.field("phone").value
        user.mail = rec.field("mail").value
        user.char_for_offer_symbol = rec.field("char_for_offer_symbol").value
        user.male = rec.field("male").value
        user.id = rec.field("id").value
        user.business_symbol = rec.field("business_symbol").value
