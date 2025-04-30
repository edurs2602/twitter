from django.db import models
from user.models import User
from core.models import CoreModel


class Post(CoreModel):
    user = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE,
        to_field='id'
    )

    text = models.TextField(
        max_length=280,
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='posts_images/',
        null=True,
        blank=True
    )

    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )

    def __str__(self):
        return f'Post by {self.user.username}'