# Generated by Django 4.2.11 on 2024-05-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("club_pages", "0022_alter_club_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="activityform",
            name="status",
            field=models.CharField(
                choices=[
                    ("WAITING", "waiting"),
                    ("ACCEPTED", "accepted"),
                    ("REJECTED", "rejected"),
                ],
                default="WAITING",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="status",
            field=models.CharField(
                choices=[
                    ("WAITING", "waiting"),
                    ("ACCEPTED", "accepted"),
                    ("REJECTED", "rejected"),
                ],
                default="WAITING",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="club",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
