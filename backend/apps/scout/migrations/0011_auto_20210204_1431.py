# Generated by Django 3.0.4 on 2021-02-04 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0010_auto_20210202_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasource',
            name='schema',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='schema',
            field=models.TextField(blank=True, null=True),
        ),
    ]
