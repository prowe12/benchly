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

# The models, which are represented as classes that inherit from
# django.db.models.Model
# Each class variable below represents a database field in the model.
# We need to tell Django what type of data each field holds
# e.g. CharField for character fields and DateTimeField for datetimes
class ClimInputs(models.Model):
    """
    Inputs to the climate model
    """
    scenario = models.PositiveIntegerField()
    start_year = models.PositiveIntegerField()
    final_emiss = models.FloatField()

class ClimOutputs(models.Model):
    """
    Outputs from the climate model
    """
    scenario = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    atmos_co2 = models.FloatField()
    ocean_co2 = models.FloatField()




# class PlotTimeSeries(models.Model):
#     """
#     For a given scenario, plot a climate variable as a function of year
#     """

# class DisplayClimVars(models.Model):
#     """
#     Display climate variables for a given scenario and year
#     """
