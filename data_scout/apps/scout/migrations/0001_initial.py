# Generated by Django 3.0.4 on 2020-03-16 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=512)),
                ('kwargs', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('sink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scout.DataSource')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('input', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_input', to='scout.DataSource')),
                ('output', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_output', to='scout.DataSource')),
            ],
        ),
        migrations.CreateModel(
            name='Transformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transformation', models.CharField(max_length=512)),
                ('kwargs', models.TextField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scout.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=512)),
                ('field_left', models.CharField(max_length=1024)),
                ('field_right', models.CharField(max_length=1024)),
                ('join_query', models.TextField()),
                ('data_source_left', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='join_data_source_left', to='scout.DataSource')),
                ('data_source_right', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='join_data_source_right', to='scout.DataSource')),
            ],
        ),
        migrations.CreateModel(
            name='FlowStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='scout.Flow')),
                ('join', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='scout.Join')),
                ('recipe', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='scout.Recipe')),
            ],
        ),
    ]
