# Generated by Django 3.2.7 on 2023-03-20 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_message_room_topic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='room',
            new_name='post',
        ),
    ]