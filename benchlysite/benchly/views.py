from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Display, Timeseries, ClimInputs, ClimOutputs


def index(request):
    latest_list = ClimInputs.objects.all()
    # order_by('user')[:]
    context = {
        'latest_list': latest_list,
    }
    # Wordier method:
    # template = loader.get_template('benchly/index.html')
    # return HttpResponse(template.render(context, request))
    # Shortcut method:
    return render(request, 'benchly/index.html', context)


def detail(request, scenario):
    question = get_object_or_404(ClimInputs, scenario=scenario)
    return render(request, 'benchly/detail.html', {'question': question})

def results(request, scenario, year):
    # response = "Scenario %s."
    # return HttpResponse(response % scenario)
    question = get_object_or_404(ClimInputs, scenario=scenario)
    return render(request, 'benchly/results.html', {'question': question,'year':year})

def vote(request, scenario):
    question = get_object_or_404(ClimInputs, scenario=scenario)
    try:
        selected_choice = question.climoutputs_set.get(year=request.POST['choice'])
    except (KeyError, ClimOutputs.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'benchly/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # selected_choice.year += 1
        # selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # return HttpResponseRedirect(reverse('results', args=(selected_choice.year)))
        return HttpResponseRedirect(reverse('results', args=(question.scenario,request.POST['choice'])))