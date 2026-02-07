"""
Migration 3/4: M2M CustomUser — user_permissions.

Creates 1 table: places_remember_customuser_user_permissions.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("places_remember", "0002_customuser_groups"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
