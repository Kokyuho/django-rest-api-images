# Generated by Django 3.0.3 on 2021-06-27 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_list', models.CharField(max_length=200)),
                ('r_list', models.CharField(max_length=200)),
                ('g_list', models.CharField(max_length=200)),
                ('b_list', models.CharField(max_length=200)),
                ('completed', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
