from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "first_name")

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data["email"],
                                        password=validated_data["password"],
                                        first_name=validated_data.get("first_name", ""))
        return user

class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
