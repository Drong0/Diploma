# Generated by Django 4.1.4 on 2023-05-14 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0007_response_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="response",
            name="status",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
