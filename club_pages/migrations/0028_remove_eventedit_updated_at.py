# Generated by Django 4.2.11 on 2024-05-04 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("club_pages", "0027_eventedit_event"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventedit",
            name="updated_at",
        ),
    ]
