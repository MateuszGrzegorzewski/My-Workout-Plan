# Generated by Django 4.1.4 on 2023-01-15 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_alter_training_series"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="plan",
            constraint=models.UniqueConstraint(
                fields=("user", "name", "training"), name="unique_training_of_plan"
            ),
        ),
    ]
