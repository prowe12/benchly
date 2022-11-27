from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from plotly.offline import plot
from plotly.graph_objs import Scatter
import numpy as np

from .models import Display, Timeseries, ClimInputs, ClimOutputs


def index(request):
    # default values to prevent bombing
    disp_scenario=1
    year=2050

    # get scenario from GET params
    climvar = request.GET.get('climvar', None)
    if climvar is None:
        # raise httperror
        return
    scenarios = [
        i for i in range(1,17) if request.GET.get(f'scenario{i}', None) is not None
    ]

    # query database
    climvarvals = []
    years=[]
    climateinputs = ClimInputs.objects.all()
    for scenario in scenarios:
        # TODO: make this parallel processed or something
        cinp = get_object_or_404(ClimInputs, scenario=scenario)
        coutp = cinp.climoutputs_set.all()
        climvarvals.append([getattr(x, climvar) for x in coutp])
        years.append([x.year for x in coutp])

    disp_inp = get_object_or_404(ClimInputs, scenario=disp_scenario)
    disp_outyear = disp_inp.climoutputs_set.get(year=year)

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

    context = {
        'climateinputs': climateinputs,
        'years': years,
        'scenario': scenarios,
        'climvar': climvar,
        'disp_scenario': disp_scenario,
        'year': year,
        'plot_div': plot_div,
        'disp_outyear': disp_outyear,
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

