"""
Test Factory for creating fake objects for testing
"""
import factory
from service.models import Account
from factory.fuzzy import FuzzyChoice, FuzzyDate
from datetime import date

class AccountFactory(factory.Factory):
    """Creates fake Accounts"""

    class Meta:
        model = Account

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    email = factory.Faker("email")
    address = factory.Faker("address")
    phone_number = factory.Faker("phone_number")
    date_joined = FuzzyDate(date(2000, 1, 1))
