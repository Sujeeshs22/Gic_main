from django.db import models
from common_config_app.models import AuditModel
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(AuditModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.email
