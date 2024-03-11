from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserAddressViewSet, UserProfileViewSet, UserViewSet

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"userprofile", UserProfileViewSet, basename="userprofile")
router.register(r"useraddresses", UserAddressViewSet, basename="useraddresses")

urlpatterns = [
    path(r"", include(router.urls)),
]
