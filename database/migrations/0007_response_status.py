# Generated by Django 4.1.4 on 2023-05-12 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0006_remove_specialization_skills_skill_specialization"),
    ]

    operations = [
        migrations.AddField(
            model_name="response",
            name="status",
            field=models.BooleanField(default=False),
        ),
    ]
