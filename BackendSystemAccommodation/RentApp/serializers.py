from rest_framework import viewsets
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from RentApp.models import User


class UserSerializer(ModelSerializer):
    avatar_user = SerializerMethodField(source='avatar_user')
    def get_avatar_user(self, user):
        if user.avatar_user:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(user.avatar_user)
            return user.avatar_user.url
        return None
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar_user', 'phone', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()
        return user