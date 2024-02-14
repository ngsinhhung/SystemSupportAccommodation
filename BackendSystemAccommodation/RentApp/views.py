import cloudinary.uploader
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from RentApp.models import User, Accommodation, Image, Post, CommentPost, Follow
from RentApp.serializers import UserSerializer, ImageSerializer, AccommodationSerializer, \
    CommentPostSerializer, PostSerializer, FollowSerializer


# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny, ]

    # def get_permissions(self):
    #     if self.action in ['detail_user', 'update_user']:
    #         return [permissions.IsAuthenticated()]
    #     return self.permission_classes

    @action(methods=['POST'], detail=False, url_path='register')
    def register_user(self, request):
        try:
            data = request.data
            role = request.data.get('role')
            avatar = request.data.get('avatar_user')

            if role in [User.Role.ADMIN]:
                new_user = User.objects.create_user(
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    username=data.get('username'),
                    email=data.get('email'),
                    password=data.get('password'),
                    phone=data.get('phone'),
                    role=role,
                )
                return Response(data=UserSerializer(new_user, context={'request': request}).data,
                                status=status.HTTP_201_CREATED)

            if role in [User.Role.HOST, User.Role.TENANT] and not avatar:
                return Response({'error': 'Avatar user not found'}, status=status.HTTP_400_BAD_REQUEST)

            res = cloudinary.uploader.upload(data.get('avatar_user'), folder='avatar_user/')

            new_user = User.objects.create_user(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password'),
                phone=data.get('phone'),
                role=role,
                avatar_user=res['secure_url'],
            )
            return Response(data=UserSerializer(new_user, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({'error': 'Error creating user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], detail=False, url_path='detail')
    def detail_user(self, request):
        try:
            current_user = User.objects.get(username=request.user)
            data = UserSerializer(current_user, context={'request': request}).data
            data['followers'] = Follow.objects.filter(follow_id=current_user.id).count()
            data['following'] = Follow.objects.filter(user_id=current_user.id).count()
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"Error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['PATCH'], detail=False, url_path='update')
    def update_user(self, request):
        try:
            data = request.data
            user_instance = User.objects.get(username=request.user)

            for key, value in data.items():
                setattr(user_instance, key, value)
            if data.get('avatar_user') is None:
                pass
            else:
                avatar_file = data.get('avatar_user')
                res = cloudinary.uploader.upload(avatar_file, folder='avatar_user/')
                user_instance.avatar_user = res['secure_url']
            user_instance.save()
            return Response(data=UserSerializer(user_instance, context={'request': request}).data,
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"Error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], url_path='current_user', url_name='current_user', detail=False)
    def current_user(self, request):
        return Response(UserSerializer(request.user).data)

    @action(methods=['POST'], detail=False, url_path='follow')
    def follow(self, request):
        try:
            queries = self.queryset
            user_id = request.query_params.get('user_id')
            user_follow = queries.get(pk=user_id)
            user = request.user
            follow, followed = Follow.objects.get_or_create(user=user, follow=user_follow)
            if not followed:
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(data=FollowSerializer(follow).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], detail=False, url_path='follower')
    def follower(self, request):
        try:
            user = request.user
            userid = User.objects.get(username=user).id
            followers = Follow.objects.filter(follow_id=userid)
            follower_array = []
            for follower in followers:
                follower_array.append(follower.user_id)
            dataUser = {
                'user': str(user),
                'followers': follower_array
            }
            return Response(dataUser, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], detail=False, url_path='following')
    def following(self, request):
        try:
            user = request.user
            userid = User.objects.get(username=user).id
            following_user = Follow.objects.filter(user_id=userid)
            following_array = []
            for follower in following_user:
                following_array.append(follower.follow_id)
            dataUser = {
                'user': str(userid),
                'following': following_array
            }
            return Response(dataUser, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PostViewSet(viewsets.ViewSet, generics.ListAPIView, generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    @action(methods=['POST'], detail=False, url_path='create')
    def create_post(self, request):
        try:
            user = request.user
            data = request.data
            if user.role in ["HOST"]:
                post_instance = Post.objects.create(
                    content=data.get('content'),
                    user_post=user,
                    district=data.get('district'),
                    city=data.get('city'),
                    number_of_people=data.get('number_of_people'),
                    cost=data.get('rent_cost'),
                    is_host_post=True
                )
                accommodation = Accommodation.objects.create(
                    owner=request.user,
                    address=data.get('address'),
                    district=data.get('district'),
                    city=data.get('city'),
                    number_of_people=data.get('number_of_people'),
                    rent_cost=data.get('rent_cost'),
                    latitude=data.get('latitude'),
                    longitude=data.get('longitude'),
                    post=post_instance
                )
                image_instance = None
                if len(request.FILES.getlist('image')) < 3:
                    return Response({"Error": "You must upload at least THREE image"})
                else:
                    for file in request.FILES.getlist('image'):
                        res = cloudinary.uploader.upload(file, folder='post_image/')
                        image_url = res['secure_url']
                        image_instance = Image.objects.create(
                            image=image_url,
                            post=post_instance
                        )
                    return Response(data=PostSerializer(post_instance, context={'request': request}).data,
                                    status=status.HTTP_201_CREATED)
            elif user.role in ["TENANT"]:
                return Response(data=PostSerializer(
                    Post.objects.create(
                        user_post=user,
                        district=data.get('district'),
                        content=data.get('content'),
                        cost=data.get('cost'),
                        city=data.get('city'),
                        number_of_people=data.get('number_of_people'),
                        is_host_post=False
                    )
                ).data, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "User deny permission"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"Error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['POST'], detail=True, url_path='comment')
    def add_comment_post(self, request, pk):
        try:
            data = request.data
            user = request.user
            return Response(data=CommentPostSerializer(
                CommentPost.objects.create(
                    user_comment=user,
                    post=self.get_object(),
                    text=data.get('text'),
                )
            ).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"Error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentPostViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = CommentPost.objects.filter(parent_comment__isnull=True)
    serializer_class = CommentPostSerializer
    permission_classes = [permissions.AllowAny]

    @action(methods=['POST'], detail=True, url_path='reply')
    def add_reply_comment(self, request, pk):
        try:
            post_instance = Post.objects.get(pk=CommentPost.objects.get(pk=pk).post_id)
            parent_comment = CommentPost.objects.get(pk=pk)
            return Response(data=CommentPostSerializer(
                CommentPost.objects.create(
                    user_comment=request.user,
                    post=post_instance,
                    text=request.data.get('text'),
                    parent_comment=parent_comment
                )
            ).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"Error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['DELETE'], detail=True, url_path='delete')
    def delete_comment(self, request, pk):
        try:
            CommentPost.objects.get(pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"Error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AccommodationViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
