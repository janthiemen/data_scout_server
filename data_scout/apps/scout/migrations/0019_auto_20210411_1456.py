# Generated by Django 3.0.4 on 2021-04-11 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0018_auto_20210226_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproject',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='scout.Project'),
        ),
    ]
