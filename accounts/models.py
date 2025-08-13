from django.db import models
from django.contrib.postgres.fields import ArrayField

class CustomUser(models.Model):
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    face_encoding = ArrayField(
        base_field=models.FloatField(),
        size=128,
        null=True,
        blank=True
    )
    face_image = models.ImageField(upload_to='face_images/')

    def __str__(self):
        return self.username or self.email
