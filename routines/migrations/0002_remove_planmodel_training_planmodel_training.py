# Generated by Django 4.1.4 on 2023-03-08 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planmodel',
            name='training',
        ),
        migrations.AddField(
            model_name='planmodel',
            name='training',
            field=models.ManyToManyField(to='routines.trainingmodel'),
        ),
    ]
