# Generated by Django 3.2.18 on 2023-03-02 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woodapp', '0002_auto_20230302_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='summary',
            field=models.TextField(blank=True),
        ),
    ]