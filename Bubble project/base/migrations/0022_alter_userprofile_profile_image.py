# Generated by Django 4.1.7 on 2023-05-15 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_alter_chatmessage_chat_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(default='default.png', upload_to='profile_images/'),
        ),
    ]
