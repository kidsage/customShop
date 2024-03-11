from rest_framework import serializers

from .models import User, UserAddress, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fileds = [
            "id",
            "email",
            "username",
            "is_business",
            "is_active",
            "is_staff",
            "verification_code",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = UserProfile
        fields = "__all__"


class UserAddressSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = UserAddress
        fields = "__all__"
