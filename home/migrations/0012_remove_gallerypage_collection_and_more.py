# Generated by Django 4.2.6 on 2024-06-23 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_gallerypage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallerypage',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='gallerypage',
            name='image',
        ),
        migrations.RemoveField(
            model_name='gallerypage',
            name='introduction',
        ),
        migrations.AddField(
            model_name='gallerypage',
            name='subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
