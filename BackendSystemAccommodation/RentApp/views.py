import cloudinary.uploader
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from RentApp.models import User, Accommodation, Image, Post, CommentPost
from RentApp.serializers import UserSerializer, ImageSerializer, AccommodationSerializer, \
    HostPostSerializer, TennantPostSerializer


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
            return Response(data=UserSerializer(new_user, context={'request': request}).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({'error': 'Error creating user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], detail=True, url_path='detail')
    def detail_user(self, request, pk):
        try:
            current_user = User.objects.get(pk=pk)
            return Response(data=UserSerializer(current_user,context={'request': request}).data,status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"Error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(methods=['PATCH'], detail=True, url_path='update')
    def update_user(self, request, pk):
        try:
            data = request.data
            user_instance = User.objects.get(pk=pk)

            for key, value in data.items():
                setattr(user_instance, key, value)
            if data.get('avatar_user') is None:
                pass
            else:
                avatar_file = data.get('avatar_user')
                res = cloudinary.uploader.upload(avatar_file, folder='avatar_user/')
                user_instance.avatar_user = res['secure_url']
            user_instance.save()
            return Response(data=UserSerializer(user_instance, context={'request': request}).data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"Error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostViewSet(viewsets.ViewSet, generics.ListAPIView, generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = HostPostSerializer
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
                    return Response(data=HostPostSerializer(post_instance, context={'request': request}).data, status=status.HTTP_201_CREATED)
            elif user.role in ["TENANT"]:
                return Response(data=TennantPostSerializer(
                    Post.objects.create(
                        user_post=user,
                        district=data.get('district'),
                        content=data.get('content'),
                        cost=data.get('desire_cost'),
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



class AccommodationViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer

