from rest_framework import serializers

from .models import User, UserAddress, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
            # "password2",
            # "is_business",
            # "is_active",
            # "is_staff",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

        def create(self, validated_data):
            user = User.objects.create_user(
                email=validated_data["email"],
                password=validated_data["password"],
            )

            return user


class UserAddressSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = UserAddress
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer
    # addresses = UserAddressSerializer

    class Meta:
        model = UserProfile
        fields = "__all__"
