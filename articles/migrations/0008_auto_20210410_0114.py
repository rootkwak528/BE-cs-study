# Generated by Django 3.1.7 on 2021-04-09 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20210409_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='history',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='this_week',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='upcoming',
            field=models.BooleanField(default=False),
        ),
    ]
