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
    old_circuit = old_state.apps.get_model("app.Circuit").objects.only("country")
    old_driver = old_state.apps.get_model("app.Driver").objects.only("nationality")

    # * For all previous database state drivers, there does not exist a driver
    #    that is assigned with new unique set of Nationality objects.
    #    Designated using the 'deleted_at' attribute
    assert not old_driver.filter(nationality__deleted_at__isnull=True).exists()
    assert not old_circuit.filter(country__deleted_at__isnull=True).exists()

    ##############
    # * Post migration *
    new_state = migrator.apply_tested_migration(("app", "0006_reassign_nationality"))
    new_circuit = new_state.apps.get_model("app.Circuit").objects.only("country")
    new_driver = new_state.apps.get_model("app.Driver").objects.only("nationality")

    assert new_circuit.filter(country__deleted_at__isnull=True).exists()
    assert new_driver.filter(nationality__deleted_at__isnull=True).exists()

    migrator.reset()

