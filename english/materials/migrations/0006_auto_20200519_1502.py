# Generated by Django 3.0.6 on 2020-05-19 12:02

from django.db import migrations, models
import materials.models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_auto_20200519_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonplan',
            name='sample_image',
            field=models.ImageField(blank=True, null=True, upload_to=materials.models.create_filename),
        ),
    ]
