# Generated by Django 5.0.3 on 2024-05-01 02:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LibraryCollection",
            fields=[
                (
                    "collection_name",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Modes",
            fields=[
                ("mode_id", models.AutoField(primary_key=True, serialize=False)),
                ("mode_name", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="Readers",
            fields=[
                ("reader_id", models.AutoField(primary_key=True, serialize=False)),
                ("reader_name", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="Transforms",
            fields=[
                ("transform_id", models.AutoField(primary_key=True, serialize=False)),
                ("transform_name", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="Writers",
            fields=[
                ("writer_id", models.AutoField(primary_key=True, serialize=False)),
                ("writer_name", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="ReaderKVStore",
            fields=[
                ("kv_id", models.AutoField(primary_key=True, serialize=False)),
                ("key", models.CharField(max_length=256)),
                ("value", models.CharField(max_length=256)),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[("string", "String"), ("number", "Number")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "readers",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="key_values",
                        to="config_library.readers",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LoggerConfiguration",
            fields=[
                ("logger_id", models.AutoField(primary_key=True, serialize=False)),
                ("logger_name", models.CharField(max_length=256)),
                (
                    "collection_key",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="config_library.librarycollection",
                    ),
                ),
                (
                    "readers",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="config_library.readers",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TransformKVStore",
            fields=[
                ("kv_id", models.AutoField(primary_key=True, serialize=False)),
                ("key", models.CharField(max_length=256)),
                ("value", models.CharField(max_length=256)),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[("string", "String"), ("number", "Number")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "transform",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="key_values",
                        to="config_library.transforms",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WriterKVStore",
            fields=[
                ("kv_id", models.AutoField(primary_key=True, serialize=False)),
                ("key", models.CharField(max_length=256)),
                ("value", models.CharField(max_length=256)),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[("string", "String"), ("number", "Number")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "writer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="key_values",
                        to="config_library.writers",
                    ),
                ),
            ],
        ),
    ]
