from django.db import models
from django.contrib.postgres.fields import JSONField


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = JSONField(default=dict)
    updated_by = JSONField(default=dict)

    class Meta:
        abstract = True
        app_label = 'base'
