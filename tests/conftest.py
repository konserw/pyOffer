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

from src import database


@pytest.fixture(scope="session")
def db():
    try:
        database.connect(
            host_name="127.0.0.1",
            database_name="koferta_test",
            user_name="postgres",
            password="docker"
        )
    except RuntimeError:
        pytest.skip("Failed to connect to test db")
    return database


def pytest_addoption(parser):
    parser.addoption("--e2e", action="store_true", dest="e2e", default=False, help="run e2e tests")


def pytest_configure(config):
    if config.option.e2e:
        setattr(config.option, "markexpr", "e2e")
    else:
        setattr(config.option, "markexpr", "not e2e")
