# Generated by Django 3.1.7 on 2021-04-05 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='subject',
        ),
    ]
