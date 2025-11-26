import factory

from app.models import Driver, Nationality


factory.Faker.override_default_locale(locale="en_CA")


class DriverMinFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    date_of_birth = factory.Faker("date_this_century")
    nationality = factory.Faker("random_element", elements=Nationality.objects.all())

    class Meta:
        model = Driver


class DriverFactory(DriverMinFactory):
    surname = factory.Faker("last_name")
    forename = factory.Faker("first_name")
    ref = factory.LazyAttribute(lambda i: f"{i.surname.lower()}")
    code = factory.LazyAttribute(lambda j: f"{j.ref[:3].upper()}")
    url = factory.LazyAttribute(lambda k: f"https://{k.surname.lower()}{k.forename.lower()}.com/")
