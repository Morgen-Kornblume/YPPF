# Generated by Django 5.0.1 on 2024-01-18 16:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("generic", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PermissionBlacklist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "permission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auth.permission",
                        verbose_name="权限",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        to_field="username",
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "权限黑名单",
                "verbose_name_plural": "权限黑名单",
            },
        ),
    ]
