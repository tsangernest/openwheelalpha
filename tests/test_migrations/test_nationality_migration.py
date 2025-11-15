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


@pytest.mark.django_db
def test_normalize_nationality_migration(migrator):
    old_state = migrator.apply_initial_migration(("app", "0005_normalize_nationality"))
    old_driver = old_state.apps.get_model("app.Driver").objects.only("nationality")

    # * For all previous database state drivers, there does not exist a driver
    #    that is assigned with new unique set of Nationality objects.
    #    Designated using the 'deleted_at' attribute
    assert not old_driver.filter(nationality__deleted_at__isnull=True).exists()


