# Generated by Django 5.1.2 on 2024-10-28 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='facebook',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='github',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='instagram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='telegram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='twitter',
            field=models.URLField(blank=True, null=True),
        ),
    ]