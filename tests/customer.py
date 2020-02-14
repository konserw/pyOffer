import pytest
from hamcrest import assert_that, is_
from src.customer import CustomerFactory, Customer

CUSTOMER_ID = 1
SHORT_NAME = "short name"
FULL_NAME = "Full business name that is quite long"
TITLE = "Mr."
FIRST_NAME = "John"
LAST_NAME = "Doe"
ADDRESS = "255 Some street\nIn some town"


class MockDB:
    def get_customer(self, customer_id):
        assert_that(customer_id, is_(CUSTOMER_ID))
        return (CUSTOMER_ID, SHORT_NAME, FULL_NAME, TITLE, FIRST_NAME, LAST_NAME, ADDRESS)


@pytest.fixture
def customer():
    factory = CustomerFactory(MockDB())
    return factory.get_customer_from_id(CUSTOMER_ID)


class TestCustomer:
    def test_get_customer(self, customer):
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
        assert_that(customer.html_address, is_("255 Some street<br />\nIn some town"))

    def test_db_id(self, customer):
        assert_that(customer.db_id, is_("1"))

    def test_null_id(self):
        customer = Customer()
        assert_that(customer.db_id, is_("NULL"))
