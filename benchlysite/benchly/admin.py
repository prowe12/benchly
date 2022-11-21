from django.contrib import admin

# Register your models here.
from .models import Display, TimeseriesVar, Timeseries, ClimInputs, ClimOutputs

admin.site.register(Display)
admin.site.register(TimeseriesVar)
admin.site.register(Timeseries)
