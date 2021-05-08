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
import csv


def main() -> None:
    with open("price.sql", encoding='utf-8', mode='w') as price_sql:
        with open("price.csv", encoding='utf-8', mode='r') as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            for row in reader:
                code = row[0]
                price = row[1]

                price_sql.write(f"SELECT public.update_price('{code}', {price});\n")


if __name__ == '__main__':
    main()
