# Generated by Django 2.2.2 on 2019-06-23 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_youtubevideo_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='author_name',
            field=models.CharField(default='Youtuber', max_length=64),
        ),
    ]
