# Generated by Django 3.0.3 on 2021-06-27 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210627_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='output',
            field=models.CharField(default='', max_length=300),
        ),
    ]
