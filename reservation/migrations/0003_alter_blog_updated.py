# Generated by Django 4.0.1 on 2022-02-28 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_rename_user_blog_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
