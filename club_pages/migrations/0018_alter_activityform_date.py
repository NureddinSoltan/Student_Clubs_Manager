# Generated by Django 4.2.11 on 2024-04-29 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("club_pages", "0017_event_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activityform",
            name="date",
            field=models.DateTimeField(null=True),
        ),
    ]
