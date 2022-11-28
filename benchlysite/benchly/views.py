from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from plotly.offline import plot
from plotly.graph_objs import Scatter
import numpy as np
from django.db.models import Min, Max

from .models import Display, Timeseries, ClimInputs, ClimOutputs


def index(request):
    # Values that must be in the database
    defaultyear = 2100

    # get variables from GET params
    climvar = request.GET.get('climvar', 'atmos_co2')
    disp_scenario = request.GET.get('disp_scenario', 1)
    year = request.GET.get('disp_year', None)

    # TODO: The possible number of scenarios is hard-wired here. Fix this.
    scenarios = [i for i in range(1,17) if request.GET.get(f'scenario{i}', None) is not None]

    # query database
    climvarvals = []
    years = []
    climateinputs = ClimInputs.objects.all()
    for scenario in scenarios:
        # TODO: make this parallel processed or something
        # SQL: select * from ClimInputs where scenario=scenario
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


    disp_outyear = {}
    # SQL: disp_inp <-- select * from ClimInputs where scenario=disp_scenario
    disp_inp = get_object_or_404(ClimInputs, scenario=disp_scenario)

    # TODO: add elif for when year is in the database, so no need to interpolate
    # disp_outyear = disp_inp.climoutputs_set.get(year=year)

    if year == '' or year is None:
        disp_outyear['year'] = ''
        disp_yearbef = (disp_inp.climoutputs_set.get(year=defaultyear)).get_fields()
        for i,(name, value) in enumerate(disp_yearbef):
            if name != 'id' and name != 'scenario':
                disp_outyear[name] = ''
    else:
        # SQL: select [atts of climoutputs] from disp_inp natural_join climoutputs
        disp_all = disp_inp.climoutputs_set.all()

        year = float(year)
        yearmin = disp_all.all().aggregate(Min('year'))['year__min']
        yearmax = disp_all.all().aggregate(Max('year'))['year__max']
        if year < yearmin:
            year = yearmin
        elif year > yearmax:
            year = yearmax



        # Get the indices to the year before and after the years of interest
        #year = max(year, min(disp_all.get(year)))
        print(disp_all.filter(year=2100))
        # Product.objects.all().aggregate(Min('price'))
        iyear = [i for i,disp_year in enumerate(disp_all) if disp_year.year>=int(year)][0]
        if iyear <= 0:
            iyear = 1

        # Interpolate everything to the selected year
        yearbef = disp_all[iyear-1].year
        yearaft = disp_all[iyear].year
        wtaft = (year-yearbef)/(yearaft-yearbef)
        wtbef = (yearaft-year)/(yearaft-yearbef)
        disp_yearbef = (disp_inp.climoutputs_set.get(year=yearbef)).get_fields()
        disp_yearaft = (disp_inp.climoutputs_set.get(year=yearaft)).get_fields()
        for i,(name, value) in enumerate(disp_yearbef):
            if name != 'id' and name != 'scenario':
                disp_outyear[name] = round(wtbef * float(value) + wtaft * float(disp_yearaft[i][1]),4)

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

