# Generated by Django 4.1.6 on 2023-02-03 16:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="assigned_to",
            new_name="owner",
        ),
    ]
