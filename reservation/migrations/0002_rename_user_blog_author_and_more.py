# Generated by Django 4.0.1 on 2022-02-22 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='user',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='user',
            new_name='author',
        ),
    ]
