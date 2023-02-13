from django.db import models

# Create your models here.
class Booking(models.Model):
    previously_said_name = models.CharField(max_length=200)