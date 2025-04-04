# Generated by Django 4.2.5 on 2025-03-28 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProcessedFile",
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
                ("original_file", models.FileField(upload_to="uploads/")),
                (
                    "processed_file",
                    models.FileField(blank=True, null=True, upload_to="processed/"),
                ),
                (
                    "file_type",
                    models.CharField(
                        choices=[("image", "Image"), ("video", "Video")], max_length=10
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="VideoSegment",
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
                ("segment_file", models.FileField(upload_to="segments/")),
                ("start_time", models.FloatField()),
                ("end_time", models.FloatField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "processed_file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="segments",
                        to="processor.processedfile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ROI",
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
                ("roi_image", models.ImageField(upload_to="rois/")),
                ("x1", models.IntegerField()),
                ("y1", models.IntegerField()),
                ("x2", models.IntegerField()),
                ("y2", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "processed_file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rois",
                        to="processor.processedfile",
                    ),
                ),
            ],
        ),
    ]
