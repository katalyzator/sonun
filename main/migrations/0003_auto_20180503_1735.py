# Generated by Django 2.0.4 on 2018-05-03 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20180503_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letters',
            name='fullname',
            field=models.CharField(max_length=255),
        ),
    ]
