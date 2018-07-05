from json import JSONDecodeError

from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
import test_case_changes.JsonRequest as json

style_template = loader.get_template('test_case_change/style_template.html').render()

# Create your views here.
def detail(request):
    template = loader.get_template('test_case_change/index.html')
    return HttpResponse(template.render())

def response(request):
    ID = request.GET['id']
    REVISION = request.GET['revision']
    try:
        if json.get_work_item_type(ID)!="Test Case":

            response= style_template+"<form id=err><font size=5>You entered ID for the Work Item Type:\"%s\" which is not a \"Test Case\"</font></form>" \
                                %json.get_work_item_type(ID)
            return HttpResponse(response)
        elif (int(REVISION) > int(json.get_t_c_max_rev(ID))):

            REVISION = json.get_t_c_max_rev(ID)
            test_case_name = "<form id='qqq'><font size=5 background-color:black ><b>Test Case:%s  %s</b></font></form>" \
                             % (ID, json.get_t_c_name(ID, REVISION))

            response = style_template+test_case_name+"<form id='err'>The max revision %s is displayed </form>%s " \
                        %(REVISION,(json.difference2(ID, REVISION)+"</body></html>"))
            return HttpResponse(response)
        else:
            test_case_name = "<form id='qqq'><font size=5 background-color:black ><b>Test Case:%s  %s</b></font></form>" \
                             % (ID,json.get_t_c_name(ID,REVISION) )
            response = style_template + test_case_name + json.difference2(ID,REVISION)+"</body></html>"
            return HttpResponse(response)
    except (JSONDecodeError, KeyError):
        response = style_template+"<form id='err'><font size=5>Oops, something went wrong. Please check your input and try again</font></form>"
        return HttpResponse(response)
