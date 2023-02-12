import factory
from authentication.factories import UserFactory
from .models import Project
from utils.tests.base import faker


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=1))
    description = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=5))
    owner = factory.SubFactory(UserFactory)
