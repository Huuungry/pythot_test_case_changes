from json import JSONDecodeError

from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context,loader
import test_case_changes.JsonRequest as json
import test_case_changes.JsonRequest2 as json2
from test_case_changes.JsonRequest2 import Json_request

style_template = loader.get_template("test_case_change/style_template.html").render()


# Create your views here.
def detail(request):
    template = loader.get_template("test_case_change/index.html")
    return HttpResponse(template.render())


def response(request):
    ID = request.GET['id']
    REVISION = request.GET['revision']
    try:
        # while(True):
        if json.get_work_item_type(ID) != "Test Case":
            response = style_template + "<form id=err><font size=5>" \
                                        "You entered ID for the Work Item Type:\"%s\" which is not a \"Test Case\"" \
                                        "</font></form>" % json.get_work_item_type(ID)
            return HttpResponse(response)
        elif REVISION == "" or int(REVISION) > int(json.get_t_c_max_rev(ID)):
            REVISION = json.get_t_c_max_rev(ID)
            changed_by = "<form id='qqq'><font size=3 background-color:black ><b>Changed by: %s  </b></font></form>" \
                         % (json.get_t_c__changed_by(ID,REVISION))
            test_case_name = "<form id='qqq'><font size=5 background-color:black ><b>Test Case:%s  %s</b></font></form>" \
                             % (ID,json.get_t_c_name(ID,REVISION))
            max_revision = "<form id='err'>The max revision %s is displayed </form>%s " \
                           % (REVISION,(json.difference2(ID,REVISION)))
            response = style_template + test_case_name + changed_by + max_revision + "</body></html>"
            return HttpResponse(response)
        else:
            changed_by = "<form id='qqq'><font size=3 background-color:black ><b>Changed by: %s  </b></font></form>" \
                         % (json.get_t_c__changed_by(ID,REVISION))
            test_case_name = "<form id='qqq'><font size=5 background-color:black ><b>Test Case:%s  %s</b></font></form>" \
                             % (ID,json.get_t_c_name(ID,REVISION))
            response = style_template + test_case_name + changed_by + json.difference2(ID,REVISION) + "</body></html>"
            return HttpResponse(response)
    except:
        response = style_template + "<form id='err'><font size=5>Oops, something went wrong. Please check your input and try again</font></form>"
        return HttpResponse(response)


def is_int(revision):
    try:
        int(revision)
        return True
    except:
        return False


def response2(request):
    ID = request.GET['id']
    REVISION = request.GET['revision']
    try:
    # while(True):
        if json.get_work_item_type(ID) != "Test Case":
            response = style_template + "<form id=err><font size=5>" \
                                        "You entered ID for the Work Item Type:\"%s\" which is not a \"Test Case\"" \
                                        "</font></form>" % json.get_work_item_type(ID)
            return HttpResponse(response)
        else:
            if is_int(REVISION) == False or REVISION == "" or REVISION <= "0" or int(REVISION) > int(
                    json.get_t_c_max_rev(ID)):
                REVISION = json.get_t_c_max_rev(ID)
                changed_by = "<form id='qqq'><font size=3 background-color:black ><b>Changed by: %s  </b></font></form>" \
                             % (json.get_t_c__changed_by(ID,REVISION))
                test_case_name = "<form id='qqq'><font size=5 background-color:black ><b>Test Case:%s  %s</b></font></form>" \
                                 % (ID,json.get_t_c_name(ID,REVISION))
                max_revision = "<form id='err'>The max revision %s is displayed </form>%s " \
                               % (REVISION,(json.difference2(ID,REVISION)))
                response = style_template + test_case_name + changed_by + max_revision + "</body></html>"
                return HttpResponse(response)
            else:
                current = Json_request(ID,REVISION)
                previous = Json_request(ID,str(int(REVISION) - 1))
                changed_by = "<form id='qqq'><font size=3 background-color:black ><b>Changed by: %s  </b></font></form>" \
                             % (json2.get_t_c_data(current.json_work_item_revision_text)[4])
                test_case_name = "<form id='qqq'><font size=5 background-color:black ><b>Test Case:%s  %s</b></font></form>" \
                                 % (ID,json2.get_t_c_data(current.json_work_item_revision_text)[2])
                response = style_template + test_case_name + changed_by + json2.difference2(current, previous) + "</body></html>"
                return HttpResponse(response)
    except:
        response = style_template + "<form id='err'><font size=5>Oops, something went wrong. Please check your input and try again</font></form>"
        return HttpResponse(response)
