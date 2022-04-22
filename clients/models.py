from django.db import models
import uuid

# Create your models here.


class Client(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    username = models.CharField(
        max_length=100, unique=True, null=True, blank=True)
    contact = models.CharField(
        max_length=11, unique=True, null=True, blank=True)
    code = models.TextField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
