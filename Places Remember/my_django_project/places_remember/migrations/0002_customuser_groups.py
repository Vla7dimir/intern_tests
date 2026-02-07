"""
Migration 2/4: M2M CustomUser — groups.

Creates 1 table: places_remember_customuser_groups.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("places_remember", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
    ]
