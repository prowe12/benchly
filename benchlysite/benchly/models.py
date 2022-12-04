"""
From https://docs.djangoproject.com/en/4.1/intro/tutorial02/:
'A model is the single, definitive source of information about your data.
It contains the essential fields and behaviors of the data you are storing.
Django follows the DRY Principle. The goal is to define your data model
in one place and automatically derive things from it.

This includes the migrations, which are entirely derived from your models file,
and are essentially a history that Django can roll through to update your
database schema to match your current models.'

Here we have two models:
PlotTimeSeries: choose scenario and climate model variable to plot
DisplayClimVars: choose scenario and year to display output variables for.
"""
from django.db import models
from django.forms import ModelForm
import numpy as np


# Define the relational schemas
class ClimInputs(models.Model):
    """
    Inputs to the climate model
    """
    # TODO: What is the sql equivalent?  For each
    scenario = models.PositiveIntegerField(primary_key = True)
    start_year = models.PositiveIntegerField()
    final_emiss = models.FloatField()

    # Extras that don't exist in database schemas
    # TODO: We could add functions for the dependent variables
    def __str__(self):
        return str(self.scenario)
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in ClimInputs._meta.fields]

class ClimOutputs(models.Model):
    """
    Outputs from the climate model
    """
    scenario = models.ForeignKey(ClimInputs, db_column='scenario', on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    # TODO: Ben - add your new fields
    atmos_co2 = models.FloatField()
    ocean_co2 = models.FloatField()
    ocean_ph = models.FloatField()
    t_C = models.FloatField()
    t_F = models.FloatField()
    t_anomaly = models.FloatField()
    f_ha = models.FloatField()
    f_ao = models.FloatField()
    f_oa = models.FloatField()
    f_al = models.FloatField()
    f_la = models.FloatField()
    tot_ha = models.FloatField()



    def __str__(self):
        return str(self.scenario) + ': ' + str(self.year)

    # Extras that don't exist in database schemas
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in ClimOutputs._meta.fields]

    class Meta:
        """
        Make scenario and year the primary key as per
        https://stackoverflow.com/questions/16800375/how-can-i-set-two-primary-key-fields-for-my-models-in-django
        """
        constraints = [
            models.UniqueConstraint(
                fields=['scenario', 'year'], name='unique_migration_host_combination'
            )
        ]


# class Display(models.Model):
#     """
#     User inputs that the user can only choose one of
#     The user can only choose one scenario/year
#     """
#     user = models.CharField(primary_key = True, max_length=20)
#     scenario = models.ForeignKey(ClimInputs, db_column='scenario', on_delete=models.CASCADE)
#     year = models.ForeignKey(ClimOutputs, db_column='year', on_delete=models.CASCADE)
#     #year = models.PositiveIntegerField()
#     def __str__(self):
#         return str(self.user)

# class Timeseries(models.Model):
#     """
#     User inputs for displaying a time series of a particular climate variable for a scenario
#     The user can choose multiple scenarios but only one climate variable
#     The scenario can differ from the scenario in Display
#     """
#     user = models.CharField(max_length=20)
#     scenario = models.ForeignKey(ClimInputs, db_column='scenario', on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.user) + str(self.scenario)

#     class Meta:
#         """
#         Make user and scenario the primary key.
#         This allows each user to have multiple scenarios
#         """
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'scenario'], name='unique_migration_host_combination2'
#             )
#         ]



# class TimeseriesVar(models.Model):
#     """ 
#     The climate variable that the user wishes to display a time series for
#     """
#     user = models.CharField(primary_key = True, max_length=20)
#     climvar = models.CharField(max_length=20)
#     def __str__(self):
#         return str(self.user) + str(self.climvar)

