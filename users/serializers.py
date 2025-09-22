from rest_framework import serializers
from .models import User
import uuid


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def create(self, validated_data):
        
        username = str(uuid.uuid4())[:30]

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=username,  
        )
        user.is_active = False
        user.save()
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.UUIDField()

