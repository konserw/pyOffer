import unittest
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


class TestCustomer(unittest.TestCase):
    def setUp(self) -> None:
        self.factory = CustomerFactory(MockDB())

    def test_get_customer(self):
        c = self.factory.get_customer_from_id(CUSTOMER_ID)
        assert_that(c.is_valid, is_(True))
        assert_that(c.id, is_(CUSTOMER_ID))
        assert_that(c.short_name, is_(SHORT_NAME))
        assert_that(c.full_name, is_(FULL_NAME))
        assert_that(c.title, is_(TITLE))
        assert_that(c.last_name, is_(LAST_NAME))
        assert_that(c.address, is_(ADDRESS))

    def test_concated_name(self):
        c = self.factory.get_customer_from_id(CUSTOMER_ID)
        assert_that(c.concated_name, is_("Mr. John Doe"))

    def test_is_not_valid(self):
        c = Customer()
        assert_that(c.is_valid, is_(False))

    def test_html_address(self):
        c = self.factory.get_customer_from_id(CUSTOMER_ID)
        assert_that(c.html_address, is_("255 Some street<br />\nIn some town"))

    def test_db_id(self):
        c = self.factory.get_customer_from_id(CUSTOMER_ID)
        assert_that(c.db_id, is_("1"))

    def test_null_id(self):
        c = Customer()
        assert_that(c.db_id, is_("NULL"))


if __name__ == '__main__':
    unittest.main()
