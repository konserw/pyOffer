import pytest
from hamcrest import assert_that, is_


@pytest.mark.xfail
class TestOffer:
    def test_something(self):
        assert_that(True, is_(False))
