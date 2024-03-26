# from django.conf import settings
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from django.shortcuts import get_object_or_404
# from django.utils.encoding import force_bytes, force_str
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status, viewsets
from rest_framework.decorators import action

# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserAddress, UserProfile
from .serializers import UserAddressSerializer, UserProfileSerializer, UserSerializer

# from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")

            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "이미 사용중인 이메일입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {
                    "message": "아이디 생성을 완료하시려면 이메일 인증번호를 입력해주시기 바랍니다.\n감사합니다.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "유효하지 않은 인증 정보"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @action(detail=False, methods=["post"])
    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "이미 로그아웃된 사용자"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserProfileViewSet(viewsets.ModelViewSet):
    # authentication_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserAddressViewSet(viewsets.ModelViewSet):
    # authentication_classes = [IsAuthenticated]
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
