import factory
from authentication.factories import UserFactory
from projects.factories import ProjectFactory
from .models import Ticket, TicketType
from utils.tests.base import faker


class TicketTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TicketType

    title = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=1))
    project = factory.SubFactory(ProjectFactory)


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    title = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=1))
    description = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=5))
    type = factory.SubFactory(TicketTypeFactory)
    project = factory.SubFactory(ProjectFactory)
    assigned_to = factory.SubFactory(UserFactory)
    created_by = factory.SubFactory(UserFactory)
