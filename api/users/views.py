from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.serializers import (LoginResponseSerializer, LoginSerializer,
                               RegisterSerializer)


# Create your views here.
class LoginAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_summary="Login",
        request_body=LoginSerializer(),
        responses={201: LoginResponseSerializer()},
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data)


class RegisterUserAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_summary="Login",
        request_body=RegisterSerializer(),
        responses={201: RegisterSerializer()},
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data)
