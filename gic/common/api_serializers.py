from rest_framework import serializers
from .models import User


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    age = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["name", "email", "age"]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("name is given empty")
        return value

    def validate_age(self, value):
        if not (0 <= value <= 120):
            raise serializers.ValidationError("age must be between 0 and 120")
        return value
