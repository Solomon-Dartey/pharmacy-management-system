# Generated by Django 5.0.6 on 2024-08-04 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='receipt_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
