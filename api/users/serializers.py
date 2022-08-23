from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
        )


class LoginResponseSerializer(serializers.Serializer):
    token = serializers.SerializerMethodField(help_text="User token")
    user = serializers.SerializerMethodField()

    def get_user(self, user):
        return UserSerializer(user, context=self.context).data

    def get_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password"})

        return LoginResponseSerializer(instance=user, context=self.context).data


class RegisterSerializer(serializers.ModelSerializer):
    # Serializer to Register User
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password2',
            'email',
            'first_name',
            'last_name'
        )
        extra_kwargs = {
          'first_name': {'required': True},
          'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return UserSerializer(user, context=self.context).data
