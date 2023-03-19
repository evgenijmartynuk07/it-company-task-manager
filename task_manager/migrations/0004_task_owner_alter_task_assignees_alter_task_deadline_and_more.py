# Generated by Django 4.1.7 on 2023-03-19 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0003_alter_worker_position"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="owner",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="task",
            name="assignees",
            field=models.ManyToManyField(
                blank=True, related_name="tasks", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="deadline",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="task",
            name="is_completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="worker",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                verbose_name="active",
            ),
        ),
    ]
