import factory

from app.models import Driver, Nationality


factory.Faker.override_default_locale(locale="en_CA")


class DriverFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    date_of_birth = factory.Faker("date_this_century")
    nationality = factory.Faker("random_element", elements=Nationality.objects.all())

    class Meta:
        model = Driver

