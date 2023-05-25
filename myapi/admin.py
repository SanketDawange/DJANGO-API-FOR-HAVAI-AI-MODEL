from django.contrib import admin

# Register your models here.
from .models import UserDetail, UserFile, Category, Scheme, Hospital

# Register your models here.

Models = [UserDetail, UserFile, Category, Scheme, Hospital]
for model in Models:
    admin.site.register(model)