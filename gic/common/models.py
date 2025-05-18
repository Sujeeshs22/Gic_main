from django.db import models
from common_config_app.models import AuditModel


class User(AuditModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.email
