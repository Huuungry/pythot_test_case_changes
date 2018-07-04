from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
import test_case_changes.JsonRequest as json


# Create your views here.
def detail(request):
    template = loader.get_template('test_case_change/index.html')
    return HttpResponse(template.render())

def response(request):
    test_case_name = "<form id='qqq'><font size=5 background-color:black ><b>Test Case:%s  %s</b></font></form>" \
                     % (request.GET['id'],json.get_t_c_name(request.GET['id'],request.GET['revision']) )
    response = loader.get_template('test_case_change/style_template.html').render() \
               +test_case_name+ json.difference2(request.GET['id'],request.GET['revision'])+"</body></html>"
    return HttpResponse(response)
