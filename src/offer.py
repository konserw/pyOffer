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
from PySide2.QtCore import QObject
from datetime import date

from src.customer import Customer
from src.merchandise import MerchandiseListModel


class OfferFactory:
    def create_empty_offer(self, author, parent=None):
        offer = Offer(parent)
        offer.merchandise_list = MerchandiseListModel(offer)
        offer.customer = Customer()
        offer.date = date.today()
        offer.author = author
        return offer


class Offer(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.merchandise_list = None
        self.customer = None
        self.terms = {}
        self.date = None
        self.inquiry_date = None
        self.inquiry_number = None
        self.offer_id = None
        self.offer_symbol = None
        self.author = None
