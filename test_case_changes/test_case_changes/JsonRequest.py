from requests_ntlm import HttpNtlmAuth
import difflib
import requests
import json
import bs4
from xml.dom import minidom
import xml.etree.ElementTree as ET
import test_case_changes.credentials

from lxml.html.diff import htmldiff

# from test_case_changes.test_case_changes import credentials

LOGIN = test_case_changes.credentials.get_login()
PASSWORD = test_case_changes.credentials.get_password()


json_response = "test"
test_case_id = "446114"
test_case_rev = "18"

def get_json_URL(test_case_id, test_case_rev):
    json_URL = "http://tfs:8080/tfs/IMPT/_apis/wit/workitems/" + test_case_id + "/revisions/" + test_case_rev + "?v_5"
    return json_URL

def get_json_response(test_case_id, test_case_rev):
    json_URL = get_json_URL(test_case_id, test_case_rev)
    r = requests.get('%s' % json_URL,auth=HttpNtlmAuth('halamerica\\'+LOGIN,PASSWORD))
    json_response = r.content.decode('utf-8')
    return json_response

def get_t_c_data(test_case_id, test_case_rev):
    parsed_t_c_id = json.loads(get_json_response(test_case_id, test_case_rev))
    t_c_id = parsed_t_c_id['id']
    t_c_rev = parsed_t_c_id['rev']
    t_c_name = parsed_t_c_id['fields']['System.Title']
    t_c_state = parsed_t_c_id['fields']['System.State']
    return t_c_id, t_c_rev, t_c_name, t_c_state

def get_t_c_id(test_case_id, test_case_rev):
    return get_t_c_data(test_case_id, test_case_rev)[0]
def get_t_c_rev(test_case_id, test_case_rev):
    return get_t_c_data(test_case_id, test_case_rev)[1]
def get_t_c_name(test_case_id, test_case_rev):
    return get_t_c_data(test_case_id, test_case_rev)[2]
def get_t_c_state(test_case_id, test_case_rev):
    return get_t_c_data(test_case_id, test_case_rev)[3]

def parse_json(test_case_id, test_case_rev):
    parsed_lib = json.loads(get_json_response(test_case_id, test_case_rev))
    steps_xml = parsed_lib['fields']['Microsoft.VSTS.TCM.Steps']
    return steps_xml

def parse_xml(test_case_id, test_case_rev):
    document = minidom.parseString(parse_json(test_case_id, test_case_rev))
    steps = document.getElementsByTagName("step")
    html = ''
    i=0
    for step in steps:
        i=i+1
        parstring = step.getElementsByTagName("parameterizedString")
        #print("Step%s Action:%s Expected result:%s " % (str(i),parstring[0].firstChild.data,parstring[1].firstChild.data))
        #html = html+("Step%s Action:%s Expected result:%s " % (str(i),parstring[0].firstChild.data,parstring[1].firstChild.data))
        html = html + ("<form><DIV><b>Step %s</b><DIV><b> Description: </b>%s</DIV><DIV><b> Expected result: </b>%s</DIV></DIV></form>\n"
                       % (str(i), parstring[0].firstChild.data, parstring[1].firstChild.data))
    return html

def parse_html(test_case_id, test_case_rev):
    soup = bs4.BeautifulSoup(parse_xml(test_case_id, test_case_rev), "html.parser")
    #results = {} TOOODOOOOO

    return soup.get_text(separator=" ")

def difference(test_case_id, test_case_rev):
    old = parse_html(test_case_id, str((int(test_case_rev) - 1))).splitlines()
    new = parse_html(test_case_id, test_case_rev).splitlines()

    #print (old, new)
    diff_html = difflib.HtmlDiff().make_file(old, new, fromdesc='T-C %sRevision %s'%(test_case_id, str((int(test_case_rev) - 1))), todesc='T-C %sRevision %s'%(test_case_id, test_case_rev))
    diff_html = diff_html.replace('&nbsp; ','&nbsp;')
    diff_html = diff_html.replace('  &nbsp;', '&nbsp;')
    return diff_html.replace(' &nbsp;', '&nbsp;')

def difference2(test_case_id, test_case_rev):
    old = parse_xml(test_case_id, str((int(test_case_rev) - 1)))
    new =parse_xml(test_case_id, test_case_rev)
    diff_html=htmldiff(old, new)
    diff_html=diff_html.replace("<del>","<del><font color=red>")
    diff_html=diff_html.replace("</del>","</del></font>")
    diff_html=diff_html.replace("<ins>","<ins><font color=green>")
    diff_html=diff_html.replace("</ins>","</ins></font>")
    return diff_html


# print(parse_json(get_json_response(get_json_URL(test_case_id,test_case_rev))))

#print(parse_xml(test_case_id, test_case_rev))
# print( difference(test_case_id, test_case_rev))
#difference(test_case_id, test_case_rev)
print(get_t_c_id(test_case_id, test_case_rev))
print(get_t_c_rev(test_case_id, test_case_rev))
print(get_t_c_name(test_case_id, test_case_rev))
print(get_t_c_state(test_case_id, test_case_rev))