# Generated by Django 2.0.4 on 2018-05-03 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubelink',
            name='embed',
            field=models.CharField(help_text='Type the youtube embeded code, for example: X8Z8okhkjv8', max_length=20),
        ),
    ]
