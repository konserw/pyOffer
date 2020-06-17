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
from src.database import get_var
from src.merchandise import MerchandiseListModel
from src.user import User

document_width = 745
left_col_width = 140


class Column:
    def __init__(self, print: bool, width: int):
        self.print = print
        self.width = width


class PrintOptions:
    col_width_price = 90
    col_width_narrow = 70

    def __init__(self, print_no=True, print_code=True, print_description=True, print_list_price=True, print_discount=True, print_price=True, print_count=True, print_total=True):
        self.no = Column(print_no, 40)
        self.symbol = Column(print_code, 0)  # width to be calculated later
        self.list_price = Column(print_list_price, self.col_width_price)
        self.discount = Column(print_discount, self.col_width_narrow)
        self.price = Column(print_price, self.col_width_price)
        self.count = Column(print_count, self.col_width_narrow)
        self.total = Column(print_total, self.col_width_price)
        # another row:
        self.description = Column(print_description, document_width)

        self.symbol.width = document_width - sum([col.width for col in self if col.print])

    def __getitem__(self, col: int) -> Column:
        """just for easy sum of col widths"""
        if col == 0:
            return self.no
        elif col == 1:
            return self.symbol
        elif col == 2:
            return self.list_price
        elif col == 3:
            return self.discount
        elif col == 4:
            return self.price
        elif col == 5:
            return self.count
        elif col == 6:
            return self.total
        else:
            raise IndexError()


class Offer(QObject):
    def __init__(self, author: User = None, parent=None):
        super().__init__(parent)
        self.merchandise_list = None
        self.customer = Customer()
        self.terms = {}
        self.date = None
        self.inquiry_date = None
        self.inquiry_number = None
        self.id = None
        self.symbol = ""
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
        offer.date = date.today()
        offer.new_symbol()
        offer.company_address = get_var("HQ")
        offer.order_email = get_var("order email")
        return offer

    def printout(self, print_options: PrintOptions = PrintOptions()) -> str:
        style = """
    .spec { font-size: 6pt; }
    .row0 { background: #efefef; }
    .row1 { background: #dadada; }
"""

        return f"""<html>
<head>
<title>Oferta</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>
<style>{style}</style>
</head>
<body>
<table>
<thead>
<tr><td>
{self.header_table()}
</td></tr>
</thead>
<tbody>
<tr><td>
    {self.inquiry_text}
</td></tr>
<tr><td>
{self.merchanidse_table(print_options)}
</td></tr>
<tr><td>
    Podane ceny nie zawierają podatku VAT<br />
</td></tr>
<tr><td>
{self.terms_table()}
</td></tr>
<tr><td>
{self.footer()}
</td></tr>
</tbody>
</table>
</body>
</html>
"""

    def terms_table(self) -> str:
        remarks = self.remarks.replace("\n", "<br />\n")
        term_table = "<table cellspacing=3>"
        for term in self.terms.values():
            term_table += f"""
    <tr>
        <td width={left_col_width}>{term.type_description}:</td>
        <td width={document_width - left_col_width - 3}>{term.long_desc}</td>
    </tr>
"""
        if self.remarks:
            term_table += f"""
    <tr>
        <td width={left_col_width}>Uwagi:</td>
        <td width={document_width - left_col_width - 3}>{remarks}</td>
    </tr>
"""

        term_table += "</table>"
        return term_table

    def merchanidse_table(self, print_options: PrintOptions = PrintOptions()) -> str:
        merchandise_list = f"""
    <table cellspacing=0>
        <thead><tr class="header">
            <td width={print_options.no.width}><b>Lp.</b></td>
            <td width={print_options.symbol.width}><b>Towar</b></td>
            <td width={print_options.list_price.width} align=right><b>Cena kat.</b></td>
            <td width={print_options.discount.width} align=right><b>Rabat</b></td>
            <td width={print_options.price.width} align=right><b>Cena</b></td>
            <td width={print_options.count.width} align=right><b>Ilość</b></td>
            <td width={print_options.total.width} align=right><b>Wartość</b></td>
        </tr></thead>
"""
        for i, item in enumerate(self.merchandise_list.list):
            row_style = 'row0' if i % 2 else 'row1'
            merchandise_list += f"""
        <tr class="{row_style}">
            <td>{i + 1}</td>
            <td>{item.code}</td>
            <td align=right>{item.list_price:.20n} zł</td>
            <td align=right>{item.discount}%</td>
            <td align=right>{item.price:.20n} zł</td>
            <td align=right>{item.count} {item.unit}</td>
            <td align=right>{item.total:.20n} zł</td>
        </tr>
        <tr class="{row_style} spec">
            <td></td>
            <td colspan=6>{item.description}</td>
        </tr>
"""
        merchandise_list += f"""
        <tr style="font-weight:bold;">
            <td align=right colspan=6>Razem:</td>
            <td align=right>{self.merchandise_list.grand_total:.20n} zł</td>
        </tr>
    </table>
"""
        return merchandise_list

    def header_table(self) -> str:
        phone = f"Tel.: {self.author.phone}" if self.author.phone else ""
        return f"""
    <table>
    <tr>
        <td valign=top width=315>
            Oferta nr: <b>{self.symbol}</b><br />
            Z dnia: {self.date:%d.%m.%Y}<br />
            Dla:<br />
            <b>{self.customer.company_name}</b><br />
            {self.customer.html_address}<br />
            {self.customer.concated_name}
        </td>
        <td width=315>
            {self.company_address}<br />
            <b>{self.author.name}</b><br />
            {self.author.mail}<br />
            {phone}
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

    def footer(self) -> str:
        return f"""
    <p>
    <b>Zamówienia prosimy kierować na adres:</b> {self.order_email} z kopią do autora oferty.<br />
    <br />
    Łączymy pozdrowienia.
    </p>
    <p align=center style="margin-left: 500">
        Ofertę przygotował{self.author.gender_suffix}<br /><br /><br />
        {self.author.name}
    </p>
"""

