# Generated by Django 4.1.7 on 2023-03-16 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worker",
            name="position",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="workers",
                to="task_manager.position",
            ),
        ),
    ]
