# Generated by Django 3.2.7 on 2023-03-23 04:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0011_auto_20230323_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]