from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader

# Create your views here.
def detail(request):
    template = loader.get_template('test_case_change/index.html')
    return HttpResponse(template.render())

def result(request):
    response = "Your Test Case ID is %s and Revision is %s." % (request.GET['id'], request.GET['revision'])
    return HttpResponse(response)