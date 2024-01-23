from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
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

class ImageAcc(models.Model):
    image = CloudinaryField('image', null=True, blank=True)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='image_accommodation')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image_of_{self.accommodation_id}'


class BasePostModel(BaseModel):
    content = models.TextField()

    class Meta:
        abstract = True

class HostPostModel(BasePostModel):
    user_post = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_host_post')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    def __str__(self):
        return f'Post_host_{self.user_post.id}'

class TenantPostModel(BasePostModel):
    user_post = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_tenant_post')
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'Tenant_host_{self.user_post.id}'

class CommentBaseModel(BaseModel):
    text = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comment', null=True,
                                       blank=True)
    class Meta:
        abstract = True


class CommentHostPostModel(CommentBaseModel):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host_comment_post')
    host_post = models.ForeignKey(HostPostModel, on_delete=models.CASCADE, related_name='host_post_comment')

    def __str__(self):
        return f'{self.user_comment}_comment_post_{self.host_post.id}'

class CommentTenantPostModel(CommentBaseModel):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_comment_post')
    tenant_post = models.ForeignKey(TenantPostModel, on_delete=models.CASCADE, related_name='tenant_post_comment')

    def __str__(self):
        return f'{self.user_comment}_comment_post_{self.tenant_post.id}'

class Notification(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='notifications')
    notice = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notify_{self.id}_of_{self.user.username}'