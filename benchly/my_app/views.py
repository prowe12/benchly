from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
from .models import ClimInputs, ClimOutputs
#from django.http import HttpResponse

# Create your views here.
# From https://www.geeksforgeeks.org/views-in-django-python/:
# A view function is a Python function that takes a Web request and returns a Web response
# The response can be the HTML contents of a Web page, a redirect, a 404 error,
# an XML document, an image, or anything that a web browser can display.
# Django views are part of the user interface — they usually render the
# HTML/CSS/Javascript in your Template files into what you see in your browser
# when you render a web page.

def home(request):
    """
    Add a dummy graphic to the home page.
    @param request An HttpRequest object
    """
    # The data from the database to display 
    # Todo: This should be from user input -> SQL query
    clim_inputs = ClimInputs.objects.all()
    clim_outputs = ClimOutputs.objects.all()

    # The plot
    # TODO: replace dummy graphic with plot from database
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div', include_plotlyjs=False)

    context={'plot_div': plot_div,
             'clim_inputs': clim_inputs,
             'clim_outputs': clim_outputs}
    return render(request, "home.html", context)

#def index(request):
#    return HttpResponse('Hello, World!')
