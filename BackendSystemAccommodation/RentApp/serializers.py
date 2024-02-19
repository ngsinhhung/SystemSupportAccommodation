from rest_framework import viewsets
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_recursive.fields import RecursiveField

from RentApp.models import User, Accommodation, ImageAccommodation, Post, CommentPost, Follow, Notification, ImagePost

class BaseImage(ModelSerializer):
    image = SerializerMethodField(source="image")
    def get_image(self,content):
        if content.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(content.image)
            return content.image.url
        return None
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

class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

class ImageAccommodationSerializer(BaseImage):
    class Meta:
        model = ImageAccommodation
        fields = ['image', 'created_at']

class ImagePostSerializer(BaseImage):
    image = SerializerMethodField(source='image')

    class Meta:
        model = ImagePost
        fields = ['image', 'created_at']

class AccommodationSerializer(ModelSerializer):
    image = SerializerMethodField()
    class Meta:
        model = Accommodation
        fields = ['id', 'owner', 'address', 'district', 'city', 'number_of_people', 'rent_cost', 'latitude', 'longitude', 'is_rented', 'image']

    def get_image(self, obj):
        return ImageAccommodationSerializer(
            ImageAccommodation.objects.filter(accommodation_id=obj.id),
            many=True
        ).data


class PostSerializer(ModelSerializer):
    image = SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'user_post', 'content', 'caption', 'description', 'is_approved', 'image']

    def get_image(self, obj):
        return ImagePostSerializer(
            ImagePost.objects.filter(post_id=obj.id),
            many=True
        ).data


class CommentPostSerializer(ModelSerializer):
    reply_comment = RecursiveField(many=True)
    class Meta:
        model = CommentPost
        fields = ['id', 'user_comment', 'post', 'text', 'parent_comment', 'reply_comment']

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'