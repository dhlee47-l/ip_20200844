# Generated by Django 3.2 on 2022-12-18 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('single_pages', '0004_user_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='comments',
        ),
    ]
