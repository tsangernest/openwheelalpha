from django.db import models


class NationalityManager(models.Manager):
    def get_queryset(self):
        # * We never want to delete, we'll use the model manager to filter
        #    out the ones with 'deleted_at'. We can then reuse the '.objects'
        #    everywhere without needing to filter out the null values. And if
        #    we want all of it, we can use the 'include_deprecated_objects'
        return super().get_queryset().exclude(deleted_at__isnull=False)


class _DeprecateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

