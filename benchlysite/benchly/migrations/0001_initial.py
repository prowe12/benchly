# Generated by Django 4.1.3 on 2022-11-20 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClimInputs',
            fields=[
                ('scenario', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('start_year', models.PositiveIntegerField()),
                ('final_emiss', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ClimOutputs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('atmos_co2', models.FloatField()),
                ('ocean_co2', models.FloatField()),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='benchly.climinputs')),
            ],
        ),
        migrations.AddConstraint(
            model_name='climoutputs',
            constraint=models.UniqueConstraint(fields=('scenario', 'year'), name='unique_migration_host_combination'),
        ),
    ]
