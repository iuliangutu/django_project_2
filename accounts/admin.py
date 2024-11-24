from django.contrib import admin

from accounts.models import Profile, AdminRequestMessage

# Register your models here.
admin.site.register(Profile)
admin.site.register(AdminRequestMessage)