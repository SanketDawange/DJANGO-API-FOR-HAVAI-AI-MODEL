# Generated by Django 4.1.1 on 2023-04-14 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapi', '0002_userdetail_delete_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='user_files/')),
                ('fd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
