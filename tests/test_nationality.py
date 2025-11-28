import pytest

from app.models import Nationality


@pytest.mark.django_db
def test_nationality_endpoint(django_client):
    response = django_client.get(path="/nationality/")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["count"] == Nationality.objects.count()

