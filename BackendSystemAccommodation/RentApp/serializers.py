from rest_framework import viewsets
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_recursive.fields import RecursiveField

from RentApp.models import User, Accommodation, ImageAccommodation, Post, CommentPost, Follow, Notification, ImagePost, \
    CommentAccommodation


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
    followers = SerializerMethodField()
    following = SerializerMethodField()

    def get_followers(self, obj):
        current_user = obj.id
        return Follow.objects.filter(follow_id=current_user).count()

    def get_following(self, obj):
        current_user = obj.id
        return Follow.objects.filter(user_id=current_user).count()

    def get_avatar_user(self, user):
        if user.avatar_user:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(user.avatar_user)
            return user.avatar_user.url
        return None

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar_user', 'phone', 'role', 'followers', 'following']
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
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Accommodation
        fields = ['id', 'owner', 'address', 'district', 'city', 'number_of_people', 'rent_cost', 'latitude', 'longitude', 'created_at', 'is_rented', 'image','description']

    def get_image(self, obj):
        return ImageAccommodationSerializer(
            ImageAccommodation.objects.filter(accommodation_id=obj.id),
            many=True
        ).data


class PostSerializer(ModelSerializer):
    image = SerializerMethodField()
    user_post = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user_post', 'content', 'caption', 'description', 'is_approved', 'created_at',  'image']

    def get_image(self, obj):
        return ImagePostSerializer(
            ImagePost.objects.filter(post_id=obj.id),
            many=True
        ).data


class CommentPostSerializer(ModelSerializer):
    reply_comment = RecursiveField(many=True)
    user_comment = UserSerializer(read_only=True)
    class Meta:
        model = CommentPost
        fields = ['id', 'user_comment', 'post', 'text', 'parent_comment', 'created_at', 'reply_comment']


class CommentAccommodationSerializer(ModelSerializer):
    reply_comment = RecursiveField(many=True)
    user_comment = UserSerializer(read_only=True)
    class Meta:
        model = CommentAccommodation
        fields = ['id', 'user_comment', 'accommodation', 'text', 'parent_comment', 'created_at', 'reply_comment']



class SenderSerializer(BaseImage):
    avatar_user = SerializerMethodField()
    def get_avatar_user(self, user):
        if user.avatar_user:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(user.avatar_user)
            return user.avatar_user.url
        return None
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar_user']

class NotificationSerializer(ModelSerializer):
    sender = SenderSerializer()

    class Meta:
        model = Notification
        fields = '__all__'