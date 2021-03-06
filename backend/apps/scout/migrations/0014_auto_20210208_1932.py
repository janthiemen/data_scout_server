# Generated by Django 3.0.4 on 2021-02-08 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0013_join_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flowstep',
            name='flow',
        ),
        migrations.RemoveField(
            model_name='flowstep',
            name='join',
        ),
        migrations.RemoveField(
            model_name='flowstep',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='tempdatasample',
            name='data_source',
        ),
        migrations.AddField(
            model_name='join',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_joins', to='scout.DataSourceFolder'),
        ),
        migrations.DeleteModel(
            name='Flow',
        ),
        migrations.DeleteModel(
            name='FlowStep',
        ),
        migrations.DeleteModel(
            name='TempDataSample',
        ),
    ]
