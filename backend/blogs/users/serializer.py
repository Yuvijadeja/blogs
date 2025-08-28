from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, ValidationError
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise ValidationError({"type": "error", "detail": "Must include both username and password."})

        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed({"type": "error", "detail": "Unable to log in with provided credentials."})
        
        if not user.is_active:
            raise PermissionDenied({"type": "error", "detail": "User account is disabled."})

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'password', 'last_name', 'dob', 'date_joined', 'gender', 'username', 'email', 'phone', 'facebook_url', 'instagram_url', 'twitter_url', 'is_active']
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            'password': {'write_only': True}
        }
        read_only_fields = ["is_active", "date_joined"]

    def create(self, validated_data):
        validated_data['is_staff'] = False
        validated_data['is_superuser'] = False

        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])

        # Create and return the new record
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        if "username" in validated_data:
            validated_data.pop('username')
        return super().update(instance, validated_data)
