import uuid
from django.db import models


class CoreModel(models.Model):
    id = models.CharField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True,
        max_length=36
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)
