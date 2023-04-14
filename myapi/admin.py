from django.contrib import admin

# Register your models here.
from .models import UserDetail, UserFile

# Register your models here.

Models = [UserDetail, UserFile]
for model in Models:
    admin.site.register(model)