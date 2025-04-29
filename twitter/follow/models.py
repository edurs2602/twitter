from django.db import models
from user.models import User
from core.models import CoreModel


class Follow(CoreModel):
    user = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    following_user = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'following_user')

    def __str__(self):
        return f"{self.user.username} follows {self.following_user.username}"
