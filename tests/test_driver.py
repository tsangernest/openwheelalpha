from pprint import PrettyPrinter

import pytest

from app.models import Driver
from tests.factories import DriverFactory

pp = PrettyPrinter(indent=2, width=1)


@pytest.mark.django_db
def test_driver_endpoint(django_client):
    response = django_client.get(path="/driver/")
    assert response.status_code == 200

    json_response = response.json()
    assert json_response["status"] == 200
    assert json_response["count"] == Driver.objects.count()


@pytest.mark.django_db
def test_driver_endpoint_create(django_client):
    post_payload = {
        "surname": "Dayne",
        "date_of_birth": "1281-01-01",
        "ref": "The Sword of the Morning.",
        "nationality_id": 3545,
    }
    response = django_client.post(path="/driver/", data=post_payload)
    json_response = response.json()
    assert Driver.objects.count() == 1
    assert json_response["status"] == 201
    json_data: dict = json_response["data"]

    # Attributes in the post payload
    assert json_data["surname"] == post_payload["surname"]
    assert json_data["date_of_birth"] == post_payload["date_of_birth"]
    assert json_data["ref"] == post_payload["ref"]
    assert json_data["nationality"] == post_payload["nationality_id"]

    # Attributes left blank in post payload
    assert json_data["forename"] == post_payload.get("forename", "")
    assert json_data["number"] == post_payload.get("number", "")
    assert json_data["code"] == post_payload.get("code", "")
    assert json_data["url"] == post_payload.get("url", "")

    # Attributes generated
    assert json_data["id"] == Driver.objects.first().id
    print(f"\n\n{Driver.objects.first().uuid=}\n")
    # response from a POST method never returns UUID
    with pytest.raises(expected_exception=KeyError):
        assert json_data["uuid"]
    print(f"\n\n")
    pp.pprint(json_data)


@pytest.mark.django_db
def test_driver_endpoint_customise_return_data(django_client):
    DriverFactory.create()
    response = django_client.get(path="/driver/")
    json_data = response.json()["data"][0]
    expected_output = {"id", "surname", "forename"}
    assert expected_output.issubset(json_data.keys())
    assert set(json_data.keys()).issubset(Driver.objects.values().first().keys())

