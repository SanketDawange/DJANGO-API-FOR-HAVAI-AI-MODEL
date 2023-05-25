# Generated by Django 4.1.6 on 2023-05-25 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0008_category_hospital_scheme'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='scheme',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapi.scheme'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheme',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapi.category'),
            preserve_default=False,
        ),
    ]
