# Generated by Django 4.1.3 on 2022-12-18 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_rename_slug_category_slug1'),
        ('single_pages', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='comments',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.comment'),
        ),
    ]
