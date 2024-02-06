from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        abstract = True
class User(AbstractUser):
    avatar_user = CloudinaryField('avatar', null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    class Role(models.TextChoices):
        TENANT = "TENANT", ('Người thuê')
        ADMIN = 'ADMIN', ('Quản trị viên')
        HOST = 'HOST', ('Chủ nhà')

    role = models.CharField(max_length=6, choices=Role.choices, null=False)
    def get_role(self) -> role:
        return self.Role(self.role)
    def __str__(self):
        return self.username

class Follow(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower')
    follow = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following')

class Accommodation(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accommodation')
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    number_of_people = models.PositiveSmallIntegerField(default=1)
    rent_cost = models.PositiveIntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_verified = models.BooleanField(default=False, choices=[(True, 'Verified'), (False, 'Not Verified')])
    is_rented = models.BooleanField(default=False, choices=[(True, 'Rented'), (False, 'Not Rent')])
    post = models.OneToOneField('Post', on_delete=models.CASCADE)
    def __str__(self):
        return f'Accommodation_{self.owner.username}'

class Image(models.Model):
    image = CloudinaryField('image', null=True, blank=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="host_post_image")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image_of_{self.post_id}'

class Post(BaseModel):
    user_post = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    content = models.TextField()
    district = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    number_of_people = models.PositiveSmallIntegerField(null=True)
    cost = models.PositiveIntegerField(null=True)
    is_host_post = models.BooleanField()
    is_approved = models.BooleanField(default=False, choices=[(True, 'Approved'), (False, 'Not Approved')])

    def __str__(self):
        return f'Post_user_{self.user_post.id}'

class CommentPost(BaseModel):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment', unique=False)
    text = models.TextField()
    parent_comment = models.ForeignKey('CommentPost', on_delete=models.CASCADE, related_name='reply_comment', null=True, blank=True)

    def __str__(self):
        return f'Comment_post_{self.post.id}'


class Notification(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='notifications')
    notice = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notify_{self.id}_of_{self.user.username}'