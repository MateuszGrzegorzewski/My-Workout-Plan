# Generated by Django 4.1.4 on 2023-02-09 18:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0004_plan_unique_training_of_plan"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Training",
            new_name="TrainingResult",
        ),
    ]
