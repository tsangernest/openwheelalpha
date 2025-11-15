from http import HTTPStatus
import pytest

from app.models import Driver


@pytest.mark.django_db
def test_driver_endpoint(c):
    response = c.get(path="/driver/")
    assert response.status_code == HTTPStatus.OK

    json_response = response.json()
    assert json_response["count"] == Driver.objects.count()

