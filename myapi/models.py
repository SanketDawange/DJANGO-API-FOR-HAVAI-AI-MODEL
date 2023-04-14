from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=5)
    contact = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=20)

    def __str__(self):
        return self.name



class UserFile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='user_files/')

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
    def delete(self, *args, **kwargs):
        # Delete the associated media file
        storage, path = self.file.storage, self.file.path
        print(f"Deleting file at {path}")
        super(UserFile, self).delete(*args, **kwargs)
        try:
            storage.delete(path)
            print(f"File at {path} deleted successfully")
        except Exception as e:
            print(f"Error deleting file at {path}: {str(e)}")


@receiver(pre_delete, sender=User)
def delete_fd_files(sender, instance, **kwargs):
    for fd_file in instance.files.all():
        file_path = fd_file.file.path
        if os.path.exists(file_path):
            os.remove(file_path)