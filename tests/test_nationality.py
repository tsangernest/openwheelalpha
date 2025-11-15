from http import HTTPStatus
import pytest

from app.models import Nationality


@pytest.mark.django_db
def test_nationality_endpoint(c):
    response = c.get(path="/nationality/")
    assert HTTPStatus.OK == response.status_code
    json_response = response.json()
    assert json_response["count"] == Nationality.objects.count()

