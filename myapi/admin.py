from django.contrib import admin

# Register your models here.
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass