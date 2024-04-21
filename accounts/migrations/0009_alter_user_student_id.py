# Generated by Django 5.0.2 on 2024-04-20 12:56

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_user_student_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="student_id",
            field=models.PositiveIntegerField(
                max_length=9,
                null=True,
                unique=True,
                validators=[accounts.models.validate_length],
            ),
        ),
    ]