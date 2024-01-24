from django.contrib import admin

from RentApp.models import User, Accommodation, HostPost

# Register your models here.
admin.site.register(User),
admin.site.register(HostPost),
admin.site.register(Accommodation),
