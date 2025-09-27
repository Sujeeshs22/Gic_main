from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username", max_length=150)
    email = serializers.EmailField(source="user.email")
    age = serializers.IntegerField(required=False)

    class Meta:
        model = Profile
        fields = ["name", "email", "age"]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty")
        return value

    def validate_age(self, value):
        if value is not None and not (0 <= value <= 120):
            raise serializers.ValidationError("Age must be between 0 and 120")
        return value
