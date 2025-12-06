from functools import cached_property
from uuid import uuid4

from django.db import models

from app.managers import _DeprecateManager, NationalityManager


class Nationality(models.Model):
    demonym = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    # More so for filtering rows
    deleted_at = models.DateTimeField(blank=True, null=True)

    # Managers for top level filtering
    objects = NationalityManager()
    include_deprecated_objects = _DeprecateManager()

    class Meta:
        ordering = ["demonym"]

    def __str__(self):
        return f"{self.demonym}"


class Driver(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    ref = models.CharField(blank=True, max_length=255)
    number = models.CharField(blank=True, max_length=255)
    code = models.CharField(blank=True, max_length=6)
    forename = models.CharField(blank=True, max_length=255)
    surname = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True)
    nationality = models.ForeignKey(to="Nationality", on_delete=models.DO_NOTHING, blank=True)
    url = models.URLField(blank=True)

    class Meta:
        ordering = ["id"]

    @cached_property
    def display_fields(self):
        # UUID is internal use only
        fields = [d.name for d in Driver._meta.get_fields()]
        fields.remove("uuid")
        return fields

    def __str__(self):
        return f"{self.code}, {self.number}, {self.surname}, {self.forename}"


class Circuit(models.Model):
    ref = models.CharField(blank=True, max_length=255)
    name = models.CharField(max_length=255)
    location = models.CharField(blank=True, max_length=255)
    country = models.ForeignKey(to="Nationality", on_delete=models.DO_NOTHING, blank=True)
    longitude = models.DecimalField(blank=True, max_digits=32, decimal_places=16)
    latitude = models.DecimalField(blank=True, max_digits=32, decimal_places=16)
    altitude = models.IntegerField(blank=True, help_text="Measured in meters")
    url = models.URLField(blank=True)

    class Meta:
        ordering = ["id"]

    @cached_property
    def coordinates(self):
        return f"{self.longitude}, {self.latitude}"

    def __str__(self):
        return f"{self.name}"


class Race(models.Model):
    name = models.CharField(max_length=255)
    track = models.ForeignKey(to="Circuit", on_delete=models.DO_NOTHING)
    date_of_race = models.DateField()
    season_round_number = models.SmallIntegerField()
    url = models.URLField(blank=True)

    class Meta:
        ordering = ["-date_of_race"]

    def __str__(self):
        return f"{self.date_of_race.year} - {self.name} - {self.season_round_number}"


class LapTime(models.Model):
    race = models.ForeignKey(to="Race", on_delete=models.DO_NOTHING, related_name="lap_times")
    driver = models.ForeignKey(to="Driver", on_delete=models.DO_NOTHING, related_name="lap_times")
    lap_number = models.PositiveIntegerField()
    race_position = models.PositiveIntegerField()
    time = models.DurationField(blank=True, null=True)

    class Meta:
        ordering = ["-race"]

    def __str__(self):
        return f"{self.race}, {self.driver}, lap_number={self.lap_number}, position={self.race_position}"
