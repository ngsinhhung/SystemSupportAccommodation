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
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following')

class Accommodation(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accommodation')
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    number_of_people = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_verified = models.BooleanField(default=False, choices=[(True, 'Verified'), (False, 'Not Verified')])
    is_rented = models.BooleanField(default=False, choices=[(True, 'Rented'), (False, 'Not Rent')])

    def __str__(self):
        return f'Accmmodation_{self.owner.username}'

class Image(models.Model):
    image = CloudinaryField('image', null=True, blank=True)
    # accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='image_accommodation')
    host_post = models.ForeignKey('HostPost', on_delete=models.CASCADE, related_name="host_post_image")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image_of_{self.host_post_id}'


class BasePostModel(BaseModel):
    content = models.TextField()
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True

class HostPost(BasePostModel):
    user_post = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_host_post')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='accommodation_host_post')
    def __str__(self):
        return f'Post_host_{self.user_post.id}'

class TenantPost(BasePostModel):
    user_post = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tenant_post')
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'Tenant_host_{self.user_post.id}'

class CommentBaseModel(BaseModel):
    text = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comment', null=True,
                                       blank=True)
    class Meta:
        abstract = True


class CommentHostPost(CommentBaseModel):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host_comment_post')
    host_post = models.ForeignKey(HostPost, on_delete=models.CASCADE, related_name='host_post_comment')

    def __str__(self):
        return f'{self.user_comment}_comment_post_{self.host_post.id}'

class CommentTenantPostModel(CommentBaseModel):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_comment_post')
    tenant_post = models.ForeignKey(TenantPost, on_delete=models.CASCADE, related_name='tenant_post_comment')

    def __str__(self):
        return f'{self.user_comment}_comment_post_{self.tenant_post.id}'

class Notification(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='notifications')
    notice = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notify_{self.id}_of_{self.user.username}'