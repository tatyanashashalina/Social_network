# Generated by Django 4.0 on 2022-02-15 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='edited',
            field=models.BooleanField(default=False, verbose_name='edited'),
        ),
    ]
