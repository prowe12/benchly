# Generated by Django 4.1.3 on 2022-11-21 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('benchly', '0003_alter_climoutputs_scenario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='display',
            name='year',
            field=models.ForeignKey(db_column='year', on_delete=django.db.models.deletion.CASCADE, to='benchly.climoutputs'),
        ),
    ]