from pathlib import Path
from pytest import fixture

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client


@fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        # readable style
        # fixtures_path = Path("/app/tests/fixtures/")
        # fixtures = [f for f in fixtures_path.glob("*.json")]
        # for f in fixtures:
        #     call_command("loaddata",f, app_label="app.nationality", verbosity=3, format="json", force_color=True)

        # stupid style
        # fixtures_path = Path("/app/tests/fixtures/")
        # fixtures = [call_command("loaddata",f, app_label="app.nationality", verbosity=3, format="json", force_color=True) for f in fixtures_path.glob("*.json")]        fixtures_path = Path("/app/tests/fixtures/")

        # most wtf style
        [call_command(
            "loaddata",
            f,
            app_label="app.nationality",
            verbosity=3,
            format="json",
            force_color=True,
        ) for f in Path("/app/tests/fixtures/").glob("*.json")]


@fixture
def rest_client():
    u = User.objects.create(
        is_active=True,
        first_name="test_open_first",
        last_name="test_open_last",
        email="openwheeltestuser@test.ca",
        username="openwheeltestuser",
    )
    c = Client()
    c.force_login(user=u)
    yield c

