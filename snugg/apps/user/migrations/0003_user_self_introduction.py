# Generated by Django 4.0.2 on 2022-07-17 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_remove_user_is_admin_user_groups_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="self_introduction",
            field=models.TextField(blank=True, default=""),
        ),
    ]