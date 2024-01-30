from django.contrib import admin

from RentApp.models import User, Accommodation, HostPost, TenantPost

# Register your models here.
admin.site.register(User),
admin.site.register(HostPost),
admin.site.register(TenantPost),
admin.site.register(Accommodation),
