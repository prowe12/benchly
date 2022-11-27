from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from plotly.offline import plot
from plotly.graph_objs import Scatter
import numpy as np

from .models import Display, Timeseries, ClimInputs, ClimOutputs


def get_climvar_names():
    climvars = ['atmos_co2', 'ocean_co2']
    return climvars

def index(request):
    # Default values
    disp_climvars = {}

    # get variables from GET params
    climvar = request.GET.get('climvar', 'atmos_co2')
    disp_scenario = request.GET.get('disp_scenario', 1)
    year = request.GET.get('disp_year', 2050)
    if year == '':
        year = 2100
    else:
        year = float(year)
    scenarios = [
        i for i in range(1,17) if request.GET.get(f'scenario{i}', None) is not None
    ]

    print(scenarios)
    print('disp_scenario', disp_scenario)

    # query database
    climvarvals = []
    years = []
    climateinputs = ClimInputs.objects.all()
    for scenario in scenarios:
        # TODO: make this parallel processed or something
        cinp = get_object_or_404(ClimInputs, scenario=scenario)
        coutp = cinp.climoutputs_set.all()
        climvarvals.append([getattr(x, climvar) for x in coutp])
        years.append([x.year for x in coutp])

 
  

    colors = [
        'red',
        'orange',
        'yellow',
        'green',
        'cyan',
        'blue',
        'magenta',
        'black',
        'gray',
    ]

    # The plot
    if len(scenarios)==0:
        plot_div=''
    else:
        plot_div = plot({'data':
                [
                    Scatter(x=xvals, y=yvals,
                            mode='lines', name=f'Scenario {scenarios[i]}',
                            opacity=0.8, marker_color=colors[i%len(colors)]) \
                    for i,(xvals,yvals) in enumerate(zip(years,climvarvals))
                ],
                        'layout': {'xaxis': {'title': 'year'},
                        'yaxis': {'title': climvar}}},
                output_type='div', include_plotlyjs=False)


    # disp_inp <-- select * from ClimInputs where scenario=disp_scenario
    disp_inp = get_object_or_404(ClimInputs, scenario=disp_scenario)
    # disp_outyear = disp_inp.climoutputs_set.get(year=year)

    # select * from disp_inp natural_join climoutputs
    disp_all = disp_inp.climoutputs_set.all()

    # Get the indices to the year before and after the years of interest
    iyear = [i for i,disp_year in enumerate(disp_all) if disp_year.year>=int(year)][0]

    # Interpolate everything to the selected year
    yearbef = disp_all[iyear-1].year
    yearaft = disp_all[iyear].year
    wtaft = (year-yearbef)/(yearaft-yearbef)
    wtbef = (yearaft-year)/(yearaft-yearbef)
    disp_yearbef = (disp_inp.climoutputs_set.get(year=yearbef)).get_fields()
    disp_yearaft = (disp_inp.climoutputs_set.get(year=yearaft)).get_fields()
    for i,(name, value) in enumerate(disp_yearbef):
        if name != 'id' and name != 'scenario' and name != 'year':
            disp_climvars[name] = round(wtbef * float(value) + wtaft * float(disp_yearaft[i][1]),4)
    print('disp_climvars: ', disp_climvars)

    context = {
        'climateinputs': climateinputs,
        'years': years,
        'scenario': scenarios,
        'climvar': climvar,
        'disp_scenario': disp_scenario,
        'year': year,
        'plot_div': plot_div,
        'disp_outyear': disp_climvars,
    }
    return render(request, 'benchly/index.html', context)


# def extra(request, scenario=1):
#     climateinputs = ClimInputs.objects.all()
#     climvars = ['atmos_co2', 'ocean_co2']
#     cinp = get_object_or_404(ClimInputs, scenario=scenario)
#     coutp = cinp.climoutputs_set.all()
#     years = [x.year for x in coutp]
#     climvar = climvars[0]
#     year = years[0]

#     # An empty plot
#     plot_div = ''

#     context = {
#         'climateinputs': climateinputs,
#         'climvars': climvars,
#         'years': years,
#         'scenario': scenario,
#         'climvar': climvar,
#         'disp_scenario': scenario,
#         'year': year,
#         'plot_div':plot_div,
#         'disp_outyear': None,
#     }
#     # Wordier method:
#     # template = loader.get_template('benchly/index.html')
#     # return HttpResponse(template.render(context, request))
#     # Shortcut method:
#     return render(request, 'benchly/index.html', context)

