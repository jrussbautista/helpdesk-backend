import factory
from utils.tests.base import faker
from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(
        lambda _: faker.profile(fields=["username"])["username"]
    )
