import pytest

from app.models import Driver


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
        "ref": "sword_of_the_morning",
        "nationality_id": "3545",
    }
    response = django_client.post(path="/driver/", data=post_payload)
    json_response = response.json()
    assert Driver.objects.count() == 1
    assert json_response["status"] == 201
    json_data: dict = json_response["data"]
    assert json_data["surname"] == "Dayne"
    assert json_data["date_of_birth"] == "1281-01-01"
    assert json_data["nationality_id"] == 3545
    assert json_data["ref"] == "sword_of_the_morning"

