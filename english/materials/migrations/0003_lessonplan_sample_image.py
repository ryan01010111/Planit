# Generated by Django 3.0.6 on 2020-05-19 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_auto_20200518_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonplan',
            name='sample_image',
            field=models.ImageField(blank=True, null=True, upload_to='sample_images'),
        ),
    ]
