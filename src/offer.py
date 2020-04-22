# pyOffer - program for creating business proposals for purchase of items
# Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

from datetime import date

from PySide2.QtCore import QObject

from src.customer import Customer
from src.database import get_company_address, get_var
from src.merchandise import MerchandiseListModel
from src.user import User


class Offer(QObject):
    def __init__(self, author: User, parent=None):
        super().__init__(parent)
        self.merchandise_list = None
        self.customer = None
        self.terms = {}
        self.date = None
        self.inquiry_date = None
        self.inquiry_number = None
        self.id = None
        self.symbol = None
        self.author = author
        self.remarks = ""
        self.company_address = ""
        self.order_email = ""

    @property
    def inquiry_text(self) -> str:
        s = "W odpowiedzi na zapytanie"
        if self.inquiry_number:
            s += f" numer {self.inquiry_number}"
        if self.inquiry_date:
            s += f" z dnia {self.inquiry_date}"
        s += ", przedstawiamy ofertę na dostawę następujących produktów:"
        return s

    def new_symbol(self) -> None:
        self.symbol = self.author.new_offer_symbol()

    @classmethod
    def create_empty(cls, author: User, parent: QObject = None) -> Offer:
        offer = cls(author, parent)
        offer.merchandise_list = MerchandiseListModel(offer)
        offer.customer = Customer()
        offer.date = date.today()
        offer.new_symbol()
        offer.company_address = "<br />\n".join(get_company_address())
        offer.order_email = get_var("order email")
        return offer

    @property
    def document(self) -> str:
        document_width = 745
        left_col_width = 140
        col_width_price = 90
        col_width_narrow = 70
        col_width_symbol = document_width - 40 - (col_width_price * 3) - (col_width_narrow * 2) - (4*7)

        phone = f"Tel.: {self.author.phone}" if self.author.phone else ""
        style = """
    body { font-family: Arial, Helvetica, sans-serif; font-size:12; } 
    .spec { font-size: 10; }
    .row0 { background: #efefef; }
    .row1 { background: #dadada; }
"""

        merchandise_list = f"""
    <table cellspacing=0>
        <thead><tr class="header">
            <td width=40><b>Lp.</b></td>
            <td width={col_width_symbol}><b>Towar</b></td>
            <td width={col_width_price} align=right><b>Cena kat.</b></td>
            <td width={col_width_narrow} align=right><b>Rabat</b></td>
            <td width={col_width_price} align=right><b>Cena</b></td>
            <td width={col_width_narrow} align=right><b>Ilość</b></td>
            <td width={col_width_price} align=right><b>Wartość</b></td>
        </tr></thead>
"""
        for i, item in enumerate(self.merchandise_list.list):
            row_style = 'row0' if i % 2 else 'row1'
            merchandise_list += f"""
        <tr class="{row_style}">
            <td>{i + 1}</td>
            <td>{item.code}</td>
            <td align=right>{item.list_price}</td>
            <td align=right>{item.discount}</td>
            <td align=right>{item.price}</td>
            <td align=right>{item.count}</td>
            <td align=right>{item.total}</td>
        </tr>
        <tr class="{row_style} spec">
            <td></td>
            <td colspan=6>{item.description}</td>
        </tr>
"""
        merchandise_list += f"""
        <tr style="font-weight:bold;">
            <td align=right colspan=6>Razem:</td>
            <td align=right>{self.merchandise_list.grand_total}</td>
        </tr>
    </table>
"""

        remarks = self.remarks.replace("\n", "<br />\n")
        term_table = "<table cellspacing=3>"
        for term in self.terms.values():
            term_table += f"""
    <tr>
        <td width={left_col_width}>{term.type_description}:</td>
        <td width={document_width-left_col_width-3}>{term.long_desc}</td>
    </tr>
"""
        if self.remarks:
            term_table += f"""
    <tr>
        <td width={left_col_width}>Uwagi:</td>
        <td width={document_width - left_col_width - 3}>{remarks}</td>
    </tr>
</table>
"""

        doc = f"""<html>
<head>
<title>Oferta</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>
<style>{style}</style>
</head>
<body>
<table>
<thead>
<tr><td>
    <table>
    <tr>
        <td valign=top width={document_width/2}>
            Oferta nr: <b>{self.symbol}</b><br />
            Z dnia: {self.date:%d.%m.%Y}<br />
            Dla:<br />
            <b>{self.customer.full_name}</b><br />
            {self.customer.html_address}<br />
            {self.customer.concated_name}
        </td>
        <td width={document_width/2}>
            <img src=:/logos height=60><br />
            {self.company_address}<br />
            <b>{self.author.name}</b><br />
            {self.author.mail}<br />
            {phone}
        </td>
    </tr>
    <tr>
        <td colspan=2>
            <hr width=100%>
        </td>
    </tr>
    </table>
</td></tr>
</thead>
<tbody>
<tr><td>
    {self.inquiry_text}
</td></tr>
<tr><td>
    {merchandise_list}
</td></tr>
<tr><td>
    Podane ceny nie zawierają podatku VAT<br />
</td></tr>
<tr><td>
{term_table}
</td></tr>
<tr><td>
    <p>
    <b>Zamówienia prosimy kierować na adres:</b> {self.order_email} z kopią do autora oferty.<br />
    <br />
    Łączymy pozdrowienia.
    </p>
    <p align=center style="margin-left: 500">
        Ofertę przygotował{self.author.gender_suffix}<br /><br /><br />
        {self.author.name}
    </p>
</td></tr>
</tbody>
</table>
</body>
</html>
"""
        return doc
