from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from plotly.offline import plot
from plotly.graph_objs import Scatter
import numpy as np

from .models import Display, Timeseries, ClimInputs, ClimOutputs


def index(request, scenario=1):
    climateinputs = ClimInputs.objects.all()
    climvars = ['atmos_co2', 'ocean_co2']
    cinp = get_object_or_404(ClimInputs, scenario=scenario)
    coutp = cinp.climoutputs_set.all()
    years = [x.year for x in coutp]
    climvar = climvars[0]
    year = years[0]

    # An empty plot
    plot_div = ''

    context = {
        'climateinputs': climateinputs,
        'climvars': climvars,
        'years': years,
        'scenario': scenario,
        'climvar': climvar,
        'disp_scenario': scenario,
        'year': year,
        'plot_div':plot_div,
        'disp_outyear': None,
    }
    # Wordier method:
    # template = loader.get_template('benchly/index.html')
    # return HttpResponse(template.render(context, request))
    # Shortcut method:
    return render(request, 'benchly/index.html', context)

def display(request, scenario=1, climvar='atmos_co2', disp_scenario=1, year=2020):
    climateinputs = ClimInputs.objects.all()
    cinp = get_object_or_404(ClimInputs, scenario=scenario)
    coutp = cinp.climoutputs_set.all()
    years = [x.year for x in coutp]
    climvarvals = [getattr(x,climvar) for x in coutp]

    disp_inp = get_object_or_404(ClimInputs, scenario=disp_scenario)
    disp_outyear = disp_inp.climoutputs_set.get(year=year)

    # The plot
    plot_div = plot({'data':[Scatter(x=years, y=climvarvals,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
                     'layout': {'xaxis': {'title': 'year'},
                     'yaxis': {'title': climvar}}},
               output_type='div', include_plotlyjs=False)

    context = {
        'climateinputs': climateinputs,
        'years': years,
        'scenario': scenario,
        'climvar': climvar,
        'disp_scenario': disp_scenario,
        'year': year,
        'plot_div': plot_div,
        'disp_outyear': disp_outyear,
    }
    return render(request, 'benchly/index.html', context)
