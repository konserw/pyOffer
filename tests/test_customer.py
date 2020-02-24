import pytest
from hamcrest import assert_that, is_
from src.customer import Customer

CUSTOMER_ID = 1
SHORT_NAME = "short name"
FULL_NAME = "Full business name that is quite long"
TITLE = "Mr."
FIRST_NAME = "John"
LAST_NAME = "Doe"
ADDRESS = "255 Some street\nIn some town"


class FakeRecord:
    def __init__(self):
        self.dict = {
            "customer_id": CUSTOMER_ID,
            "short_name": SHORT_NAME,
            "full_name": FULL_NAME,
            "title": TITLE,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "address": "255 Some street\\nIn some town",
        }

    def value(self, key):
        return self.dict[key]


@pytest.fixture
def customer():
    c = Customer()
    c.id = CUSTOMER_ID
    c.short_name = SHORT_NAME
    c.full_name = FULL_NAME
    c.title = TITLE
    c.first_name = FIRST_NAME
    c.last_name = LAST_NAME
    c.address = ADDRESS
    return c


class TestCustomer:
    def test_customer_from_record(self, customer):
        assert_that(customer.is_valid, is_(True))
        assert_that(customer.id, is_(CUSTOMER_ID))
        assert_that(customer.short_name, is_(SHORT_NAME))
        assert_that(customer.full_name, is_(FULL_NAME))
        assert_that(customer.title, is_(TITLE))
        assert_that(customer.last_name, is_(LAST_NAME))
        assert_that(customer.address, is_(ADDRESS))

    def test_concated_name(self, customer):
        assert_that(customer.concated_name, is_("Mr. John Doe"))

    def test_is_not_valid(self):
        customer = Customer()
        assert_that(customer.is_valid, is_(False))

    def test_html_address(self, customer):
        assert_that(customer.html_address, is_(ADDRESS))

    def test_db_id(self, customer):
        assert_that(customer.db_id, is_("1"))

    def test_null_id(self):
        customer = Customer()
        assert_that(customer.db_id, is_("NULL"))

    def test_description(self, customer):
        assert_that(customer.description, is_("Mr. John Doe\nFull business name that is quite long\n255 Some street\nIn some town"))

    def test_str(self, customer):
        assert_that(str(customer), is_("Customer 1: Mr. John Doe; short name"))
