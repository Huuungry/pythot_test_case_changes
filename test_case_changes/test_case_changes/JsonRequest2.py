from requests_ntlm import HttpNtlmAuth
import difflib
import requests
import json
import bs4
from xml.dom import minidom
from lxml.html.diff import htmldiff

# import credentials
# LOGIN = credentials.get_login()
# PASSWORD = credentials.get_password()

import test_case_changes.credentials as credls
LOGIN = credls.get_login()
PASSWORD = credls.get_password()


# def get_json_URL(test_case_id, test_case_rev):
#     json_URL = "http://tfs:8080/tfs/IMPT/_apis/wit/workitems/" + test_case_id + "/revisions/" + test_case_rev + "?v_5"
#     return json_URL
def get_json_URL(test_case_id, test_case_rev):
    json_URL = "http://tfs:8080/tfs/IMPT/_apis/wit/workitems/" + test_case_id + "/revisions/" + test_case_rev + "?v_5"
    if test_case_rev == '':
        json_URL = json_URL.replace("/revisions/?v_5", "")
    return json_URL




def get_json_response(test_case_id, test_case_rev):
    json_URL = get_json_URL(test_case_id, test_case_rev)
    r = requests.get('%s' % json_URL,auth=HttpNtlmAuth('halamerica\\'+LOGIN,PASSWORD))
    json_response = r.content.decode('utf-8')
    return json_response

def parse_json(json_text):
    parsed_lib = json.loads(json_text)
    steps_xml = parsed_lib['fields']['Microsoft.VSTS.TCM.Steps']
    return steps_xml

def parse_xml(json_text):
    document = minidom.parseString(parse_json(json_text))
    steps = document.getElementsByTagName("step")
    html = ''
    i=0
    for step in steps:
        i=i+1
        parstring = step.getElementsByTagName("parameterizedString")
        try:
            #print("Step%s Action:%s Expected result:%s " % (str(i),parstring[0].firstChild.data,parstring[1].firstChild.data))
            #html = html+("Step%s Action:%s Expected result:%s " % (str(i),parstring[0].firstChild.data,parstring[1].firstChild.data))
            html = html + ("<form><DIV><b>Step %s</b><DIV><b> Description: </b>%s</DIV><DIV><b> Expected result: </b>%s</DIV></DIV></form>\n"
                           % (str(i), parstring[0].firstChild.data, parstring[1].firstChild.data))
        except AttributeError:
            pass
    return html

def parse_html(json_text):
    soup = bs4.BeautifulSoup(parse_xml(json_text), "html.parser")
    d = {}
    list = soup.find_all('form')
    for list_element in list:
        step = list_element.findChildren()[1]
        description = list_element.findChildren()[2]
        expected_result = list_element.findChildren()[2].next_sibling
        d[step.text]=[description.text, expected_result.text]
    return d

def get_t_c_data(json_text):
    parsed_t_c_id = json.loads(json_text)
    t_c_id = parsed_t_c_id['id']
    t_c_rev = parsed_t_c_id['rev']
    t_c_name = parsed_t_c_id['fields']['System.Title']
    t_c_state = parsed_t_c_id['fields']['System.State']
    t_c_changed_by = parsed_t_c_id['fields']['System.ChangedBy']
    return t_c_id, t_c_rev, t_c_name, t_c_state,  t_c_changed_by

def difference2(current, old):
    if (current.revision == "1"):
        return current.html
    elif parse_xml(old.json_work_item_revision_text) == parse_xml(current.json_work_item_revision_text):
        return "<form id=err>No steps changes in the revision %s</form>" % current.revision+parse_xml(current.json_work_item_revision_text)
    else:
        old = old.html
        new = current.html
        diff_html=htmldiff(old, new)
        diff_html=diff_html.replace("<del>","<del><font color=red>")
        diff_html=diff_html.replace("</del>","</del></font>")
        diff_html=diff_html.replace("<ins>","<ins><font color=green>")
        diff_html=diff_html.replace("</ins>","</ins></font>")
        return diff_html

class Json_request:
    def __init__(self, id, revision):

        self.id = id
        self.revision = revision
        if revision =="0":
            self.revision="1"
        # self.json_work_item_text= get_json_response(id,"")
        self.json_work_item_revision_text = get_json_response(id,self.revision)
        self.html = parse_xml(self.json_work_item_revision_text)



def get_work_item_type(json_text):
    parsed_t_c = json.loads(get_json_response(json_text))
    workitem_type = parsed_t_c['fields']['System.WorkItemType']
    return workitem_type



def get_t_c_id(test_case_id, test_case_rev):
    return get_t_c_data(test_case_id, test_case_rev)[0]

def get_t_c_rev(test_case_id, test_case_rev):
    return get_t_c_data(test_case_id, test_case_rev)[1]

def get_t_c_max_rev(test_case_id):
    parsed_t_c = json.loads(get_json_response(test_case_id, ''))
    rev_max = parsed_t_c['count']
    return str(rev_max)



def get_t_c_name(test_case_id, test_case_rev):
    return get_t_c_data(test_case_id, test_case_rev)[2]

def get_t_c_state(test_case_id, test_case_rev):
    return get_t_c_data(test_case_id, test_case_rev)[3]

def get_t_c__changed_by(test_case_id, test_case_rev):
    return get_t_c_data(test_case_id, test_case_rev)[4]




#
# print(current.json_work_item_revision_text)
# print(previous.json_work_item_revision_text)

# current = Json_request("408179","271")
# previous = Json_request("408179","200")
# print(difference2(current, previous))
