# Generated by Django 4.0.2 on 2022-07-13 06:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("qna", "0003_alter_post_accepted_answer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="content_type",
            field=models.ForeignKey(
                limit_choices_to=models.Q(
                    ("model", "Post"),
                    ("model", "Answer"),
                    ("model", "Comment"),
                    _connector="OR",
                ),
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
    ]
