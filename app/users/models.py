from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from customshop.utils.timestamp import TimeStampedModel

# from django.db.models.signals import post_save
# from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("email field must be set")
        if not password:
            raise ValueError("password field must be set")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email = models.EmailField(max_length=255, unique=True)

    is_business = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # email 인증 후에 True로 변경

    objects = UserManager()

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = [
    #     "username",
    # ]

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.email

    # @property
    # def is_staff(self):
    #     return self.is_superuser


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 프로필 관련
    image = models.ImageField(upload_to="profile", null=True)
    nickname = models.CharField(max_length=8, unique=True)
    birthday = models.DateField(null=True, blank=True)
    # addresses = models.ManyToManyField(
    #     "UserAddress", related_name="user_profile", blank=True
    # )

    class Meta:
        db_table = "user_profile"

    def __str__(self) -> str:
        return f"{self.user.email}'s Profile"


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class UserAddress(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    address_name = models.CharField(max_length=10)
    username = models.CharField(max_length=255, default=None, null=True, blank=True)
    zip_code = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = "user_address"

    def __str__(self) -> str:
        return f"{self.user.email}'s address"
