from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from plotly.offline import plot
from plotly.graph_objs import Scatter
import numpy as np
from django.db.models import Min, Max

from .models import ClimInputs, ClimOutputs


def index(request):
    # Values that must be in the database
    defaultyear = 2100

    # get variables from GET params (leave this alone Ben)
    climvar = request.GET.get('climvar', 'f_ha') # the second value is the default I think
    disp_scenario = request.GET.get('disp_scenario', 1)
    year = request.GET.get('disp_year', None)

    # TODO: The possible number of scenarios is hard-wired here. Fix this.
    scenarios = [i for i in range(1,17) if request.GET.get(f'scenario{i}', None) is not None]

    # query database
    climvarvals = []
    years = []

    # SQL: select * from ClimInputs
    climateinputs = ClimInputs.objects.all()
    for scenario in scenarios:
        # Django ORM for SQL command: select scenario,year from ClimateOutputs where scenario=scenario
        coutp = (ClimOutputs.objects.only('scenario', 'year', climvar)).filter(scenario=scenario)
        # Get x and y values for timeseries plot
        years.append([x.year for x in coutp])
        climvarvals.append([getattr(x, climvar) for x in coutp])

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
        'cornflowerblue',
        'olive',
        'tomato',
        'rosybrown',
        'cadetblue',
        'orchid',
        'purple',
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

    # Names for displaying climate variables
    climvar_names = {'atmos_co2': 'Atmospheric CO2 (GTC)',
                     'ocean_co2': 'Ocean CO2 (GTC)',
                     'ocean_ph': 'Ocean pH (GTC)',
                     't_C': 'temperature (C)',
                     't_F': 'temperature (F)',
                     't_anomaly': 'temp. anomaly (C)',
                     'f_ha': 'flux human-atmosphere (GTC)',
                     'f_ao': 'flux atmosphere-ocean (GTC)',
                     'f_oa': 'flux ocean-atmosphere (GTC)',
                     'f_al': 'flux atmosphere-land (GTC)',
                     'f_la': 'flux land-atmosphere (GTC)',
                     'tot_ha': 'total CO2 human-atmosphere (GTC)',
                     'year': 'year',
                    }

    disp_outyear = {}
    # SQL: disp_inp <-- select * from ClimInputs where scenario=disp_scenario
    disp_inp = get_object_or_404(ClimInputs, scenario=disp_scenario)

    # TODO: add elif for when year is in the database, so no need to interpolate
    # disp_outyear = disp_inp.climoutputs_set.get(year=year)

    disp_out = {}
    if year == '' or year is None:
        disp_outyear['year'] = ''
        disp_yearbef = (disp_inp.climoutputs_set.get(year=defaultyear)).get_fields()
        for i,(name, value) in enumerate(disp_yearbef):
            if name != 'id' and name != 'scenario':
                disp_outyear[name] = ''
                disp_out[climvar_names[name]] = ''
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
        # Product.objects.all().aggregate(Min('price'))
        iyear = [i for i,disp_year in enumerate(disp_all) if disp_year.year>=int(year)][0]
        if iyear <= 0:
            iyear = 1

        # Interpolate everything to the selected year
        yearbef = disp_all[iyear-1].year
        yearaft = disp_all[iyear].year
        print(yearbef)
        print(yearaft)
        wtaft = (year-yearbef)/(yearaft-yearbef)
        wtbef = (yearaft-year)/(yearaft-yearbef)
        disp_yearbef = (disp_inp.climoutputs_set.get(year=yearbef)).get_fields()
        disp_yearaft = (disp_inp.climoutputs_set.get(year=yearaft)).get_fields()
        for i,(name, value) in enumerate(disp_yearbef):
            if name != 'id' and name != 'scenario':
                res = round(wtbef * float(value) + wtaft * float(disp_yearaft[i][1]), 2)
                disp_outyear[name] = res
                disp_out[climvar_names[name]] = str(res)

    print(climvar_names)
    context = {
        'climateinputs': climateinputs,
        'years': years,
        'scenario': scenarios,
        'climvar': climvar,
        'disp_scenario': disp_scenario,
        'year': year,
        'plot_div': plot_div,
        'climvar_names': climvar_names,
        'disp_out': disp_out,
    }
    return render(request, 'benchly/index.html', context)
