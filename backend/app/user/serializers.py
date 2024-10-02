"""
Serializers for the user API view.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers

from rest_framework.exceptions import APIException

from django.contrib.auth.models import AnonymousUser
from core.models import Role, Session


class NotValidRole(APIException):
    status_code = 400
    default_detail = 'Ingrese un rol válido'
    default_code = 'role_field'


from rest_framework import serializers
from django.contrib.auth import get_user_model

from typing import Optional
from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    role_field = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['pk', 'email', 'password', 'name', 'is_active', 'role_field']
        extra_kwargs = {
            'password': {'write_only': True,},
        }

    def get_role_field(self, obj) -> Optional[str]:
        """Get the role name of the user."""
        return obj.role.role_name if obj.role else "SuperAdmin"

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class ManageUserSerializer(UserSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'is_active', 'role_field']
        extra_kwargs = {'password':{'write_only': True, 'min_length': 12},}


    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        role_name = validated_data.pop('role_field', None)
        user = get_user_model().objects.create_user(**validated_data)

        try:
            role = Role.objects.get(role_name=role_name)
        except:
            raise ValueError("Rol inválido")
        
        user.role = role
        return user


    def update(self, instance, validated_data):
        """Update and return user."""
        role_name = validated_data.pop('role_field', None)
        user = super().update(instance, validated_data)

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')


        user = get_user_model().objects.filter(email = email)

        if not user.exists():
            print("No hay")
            attrs['user'] = AnonymousUser()
            return attrs


        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            print("No correcto")
            return attrs

        attrs['user'] = user
        return attrs


class  SessionSerializer(serializers.ModelSerializer):
    """Serializer for session."""

    class Meta:
        model = Session
        fields = ['id', 'login_time', 'logout_time']
        read_only_fields = ['id', 'login_time', 'logout_time']


class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField()
