# Migration: Memory model (depends on CustomUser).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("places_remember", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Memory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("comment", models.TextField(max_length=1000)),
                ("lat", models.FloatField()),
                ("lng", models.FloatField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=models.CASCADE, related_name="memories", to="places_remember.customuser")),
            ],
            options={
                "ordering": ["-created_at"],
                "verbose_name": "memory",
                "verbose_name_plural": "memories",
            },
        ),
    ]
