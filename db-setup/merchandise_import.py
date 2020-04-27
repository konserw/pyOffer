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
    with open("merchandise.sql", encoding='utf-8', mode='w') as merchandise_sql:
        merchandise_sql.write("INSERT INTO public.merchandise(merchandise_id, code, description, unit, discount_group) VALUES\n")
        with open("price.sql", encoding='utf-8', mode='w') as price_sql:
            price_sql.write("INSERT INTO public.price(merchandise_id, value) VALUES\n")
            with open("merchandise.csv", encoding='utf-8', mode='r') as csv_file:
                reader = csv.reader(csv_file, delimiter=",")
                for i, row in enumerate(reader):
                    if i == 0:  # column headers
                        continue
                    if i > 1:
                        merchandise_sql.write(",\n")
                        price_sql.write(",\n")
                    desc = row[2]
                    #if '"' in desc:
                    #    print(desc)
                    desc = desc.replace("''", "\u2033")  # replace poor man's inch with proper unicode symbol
                    if "'" in desc:
                        print(desc)  # say what?
                        if "cal" in desc:
                            desc = desc.replace("'", "\u2033")
                        desc = desc.replace("'", "")
                    unit = "m" if row[4] == "mb." else "pc."  # by piece by default
                    merchandise_sql.write(f"({i}, '{row[0]}', '{desc}', '{unit}', '{row[1]}')")
                    price = row[3] if row[3] else 0
                    price *= 4.45  # EUR -> PLN
                    price_sql.write(f"({i}, '{price}')")

            price_sql.write(";\n")
        merchandise_sql.write(";\n")


if __name__ == '__main__':
    main()
