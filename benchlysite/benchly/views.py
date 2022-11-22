from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Display, Timeseries, ClimInputs, ClimOutputs


def index(request, scenario=1):
    climateinputs = ClimInputs.objects.all()
    climvars = ['atmos_co2', 'ocean_co2']
    cinp = get_object_or_404(ClimInputs, scenario=scenario)
    coutp = cinp.climoutputs_set.all()
    years = [x.year for x in coutp]

    climvar = climvars[0]
    year = years[0]
    context = {
        'climateinputs': climateinputs,
        'climvars': climvars,
        'years': years,
        'scenario': scenario,
        'climvar': climvar,
        'disp_scenario': scenario,
        'year': year,
    }
    # Wordier method:
    # template = loader.get_template('benchly/index.html')
    # return HttpResponse(template.render(context, request))
    # Shortcut method:
    return render(request, 'benchly/index.html', context)

def display(request, scenario=1, climvar=None, disp_scenario=1, year=None):
    climateinputs = ClimInputs.objects.all()
    climvars = ['atmos_co2', 'ocean_co2']
    cinp = get_object_or_404(ClimInputs, scenario=scenario)
    coutp = cinp.climoutputs_set.all()
    years = [x.year for x in coutp]
    if climvar is None:
        climvar = climvars[0]
    if year is None:
        year = years[0]
    context = {
        'climateinputs': climateinputs,
        'climvars': climvars,
        'years': years,
        'scenario': scenario,
        'climvar': climvar,
        'disp_scenario': disp_scenario,
        'year': year,
    }
    return render(request, 'benchly/index.html', context)
