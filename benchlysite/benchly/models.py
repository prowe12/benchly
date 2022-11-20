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

class ClimInputs(models.Model):
    """
    Inputs to the climate model
    """
    scenario = models.PositiveIntegerField(primary_key = True)
    start_year = models.PositiveIntegerField()
    final_emiss = models.FloatField()

class ClimOutputs(models.Model):
    """
    Outputs from the climate model
    """
    scenario = models.ForeignKey(ClimInputs, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    atmos_co2 = models.FloatField()
    ocean_co2 = models.FloatField()

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

# class ChoiceDisplay(models.Model):
#     """
#     User inputs for displaying climate variables for a given scenario and year
#     The user can only choose one scenario/year
#     """
#     scenario = models.ForeignKey(ClimOutputs, on_delete=models.CASCADE)
#     year = models.ForeignKey(ClimOutputs, on_delete=models.CASCADE)


# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)



