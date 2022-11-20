from django.shortcuts import render
#from plotly.offline import plot
#from plotly.graph_objs import Scatter
#from .models import ClimInputs, ClimOutputs
#from django.http import HttpResponse

# Create your views here.
# From https://www.geeksforgeeks.org/views-in-django-python/:
# A view function is a Python function that takes a Web request and returns a Web response
# The response can be the HTML contents of a Web page, a redirect, a 404 error,
# an XML document, an image, or anything that a web browser can display.
# Django views are part of the user interface — they usually render the
# HTML/CSS/Javascript in your Template files into what you see in your browser
# when you render a web page.

def home(request): #, sel_scenario=1, sel_clim_var='atmos_co2', sel_year=2100):
    """
    Add a dummy graphic print the relations to the home page
    @param request  An HttpRequest object
    @param scenario  The scenario to run
    """

    # # Selected scenario for figure
    # if (request.GET.get('scenario1')):
    #     # if request.GET.get('mytextbox') == "Scenario 1":
    #     sel_scenario = 1
    # if (request.GET.get('scenario2')):
    #     sel_scenario = 2
    # if (request.GET.get('scenario3')):
    #     sel_scenario = 3
    # if (request.GET.get('scenario4')):
    #     sel_scenario = 4

    # # Get all scenarios for the climate inputs
    # all_inputs = ClimInputs.objects.all()

    # # Get the selected inputs
    # sel_inputs = ClimInputs.objects.get(scenario=sel_scenario)

    # # Get all the tuples (years) from the output relation
    # # where the scenario is the selected scenario
    # timeseries = ClimOutputs.objects.filter(scenario=sel_scenario)

    # # From the selected output tuples, get the years column and
    # # the column of the selected climate variable
    # years = list(timeseries.values_list('year'))
    # years = [y[0] for y in years]
    # clim_var = list(timeseries.values_list(sel_clim_var))
    # clim_var = [c[0] for c in clim_var]

    # # Get the climate output variables for the selected scenario
    # # and the selected year
    # #sel_outputs = timeseries.filter(year=sel_year)
    # sel_outputs = ClimOutputs.objects.filter(scenario=sel_scenario,
    #                                          year = sel_year)

    # # The plot
    # plot_div = plot({'data':[Scatter(x=years, y=clim_var,
    #                     mode='lines', name='test',
    #                     opacity=0.8, marker_color='green')],
    #                  'layout': {'xaxis': {'title': 'year'},
    #                  'yaxis': {'title': sel_clim_var}}},
    #            output_type='div', include_plotlyjs=False)

    # context={'plot_div': plot_div,
    #          'all_inputs': all_inputs,
    #          'sel_inputs': sel_inputs,
    #          'sel_outputs': sel_outputs}
    return render(request, "home.html") #, context)

    # return HttpResponse('Hello, World!')
