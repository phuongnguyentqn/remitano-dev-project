# Generated by Django 2.2.2 on 2019-06-22 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190622_0736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youtubevideo',
            name='html',
        ),
    ]
