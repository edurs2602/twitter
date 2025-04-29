import uuid
from django.db import models


class CoreModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True,
        verbose_name="id"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True
