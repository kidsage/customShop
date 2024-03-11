from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
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
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "이미 사용중인 이메일입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))

        verification_url = f"http://127.0.0.1:8000/users/verify-email/{uid}/{token}/"
        subject = "[이메일 인증] customshop 이메일 인증 코드입니다."
        message = f"Your verification code is: {verification_url}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": "아이디 생성을 완료하시려면 이메일 인증번호를 입력해주시기 바랍니다.\n감사합니다.",
                "tokens": tokens,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="verify-email/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/",
    )
    def verify_email(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = force_str(urlsafe_base64_decode(uidb64))

        try:
            user = User.objects.get(id=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()

                return Response(
                    {"message": "이메일 인증이 완료되었습니다."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "이메일 확인 링크가 잘못되었습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            return Response(
                {"message": "사용자를 찾을 수 없습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserAddressViewSet(viewsets.ModelViewSet):
    authentication_classes = [IsAuthenticated]
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
