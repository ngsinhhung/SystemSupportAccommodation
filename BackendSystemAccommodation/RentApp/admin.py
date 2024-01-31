from django.contrib import admin

from RentApp.models import User, Accommodation, Post, CommentPost

# Register your models here.
admin.site.register(User),
admin.site.register(Post),
admin.site.register(CommentPost),
admin.site.register(Accommodation),
