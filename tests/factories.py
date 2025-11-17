import factory

from app.models import Driver, Nationality


class DriverFactory(factory.django.DjangoModelFactory):
    uuid = factory.faker.Faker("uuid4")

    class Meta:
        model = Driver

