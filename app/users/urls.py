from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserAddressViewSet, UserProfileViewSet, UserViewSet

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")
router.register(r"profile", UserProfileViewSet, basename="userprofile")
router.register(r"addresses", UserAddressViewSet, basename="useraddresses")

urlpatterns = [
    path(r"", include(router.urls)),
]
