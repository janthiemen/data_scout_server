# Generated by Django 3.0.4 on 2021-01-12 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0004_auto_20200417_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='sampling_technique',
            field=models.CharField(choices=[('top', 'Top'), ('random', 'Random'), ('stratified', 'Stratified')], default='top', max_length=64),
        ),
    ]
