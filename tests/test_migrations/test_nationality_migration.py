import pytest


@pytest.mark.django_db
def test_nationality_migration(migrator):
    old_state = migrator.apply_initial_migration(("app", "0001_nationality_and_drivers"))
    old_nationality = old_state.apps.get_model("app", "Nationality")
    assert 0 == old_nationality.objects.count()

    new_state = migrator.apply_tested_migration(("app", "0002_insert_nationality"))
    nationality = new_state.apps.get_model("app", "Nationality")
    assert 2142 == nationality.objects.count()

    migrator.reset()

