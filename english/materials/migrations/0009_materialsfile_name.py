# Generated by Django 3.0.6 on 2020-05-27 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0008_auto_20200527_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialsfile',
            name='name',
            field=models.CharField(default='koi', max_length=128),
            preserve_default=False,
        ),
    ]
