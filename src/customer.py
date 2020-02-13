#  kOferta - system usprawniajacy proces ofertowania
#  Copyright (C) 2011  Kamil 'konserw' Strzempowicz, konserw@gmail.com
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


class CustomerFactory(object):
    def __init__(self, db):
        self.db = db

    def get_customer_from_id(self, customer_id):
        t = self.db.get_customer(customer_id)
        c = Customer()
        c.id = t[0]
        c.short_name = t[1]
        c.full_name = t[2]
        c.title = t[3]
        c.first_name = t[4]
        c.last_name = t[5]
        c.address = t[6]
        return c


class Customer(object):
    def __init__(self):
        self.id = None
        self.short_name = None
        self.full_name = None
        self.title = None
        self.first_name = None
        self.last_name = None
        self.address = None

    @property
    def concated_name(self):
        return "{} {} {}".format(self.title, self.first_name, self.last_name)

    @property
    def is_valid(self):
        return self.id is not None

    @property
    def html_address(self):
        return self.address.replace("\n", "<br />\n")

    @property
    def db_id(self):
        return "NULL" if self.id is None else str(self.id)
