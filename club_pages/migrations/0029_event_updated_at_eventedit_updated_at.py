# Generated by Django 4.2.11 on 2024-05-04 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("club_pages", "0028_remove_eventedit_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name="eventedit",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
