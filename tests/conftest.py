import pytest
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        for f in Path("/app/tests/fixtures/").glob("*.json"):
             call_command("loaddata", f, "--verbosity=3", "--format=json")


@pytest.fixture
def django_client():
    u = User.objects.create(
        is_active=True,
        first_name="test_open_first",
        last_name="test_open_last",
        email="openwheeltestuser@test.ca",
        username="openwheeltestuser",
    )
    c = Client()
    c.force_login(user=u)
    return c

