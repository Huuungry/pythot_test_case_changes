from requests_ntlm import HttpNtlmAuth
import difflib
import requests
import json
from xml.dom import minidom
import xml.etree.ElementTree as ET

import credentials

LOGIN = credentials.get_login()
PASSWORD = credentials.get_password()

json_response = ""
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

def parse_json(test_case_id, test_case_rev):
    steps_xml = ""
    parsed_lib = json.loads(get_json_response(test_case_id, test_case_rev))
    steps_html = parsed_lib['fields']['Microsoft.VSTS.TCM.Steps']
    return steps_xml

def parse_xml():
    steps_html = ""
    return steps_html

def difference(test_case_id, test_case_rev):
    diff_html = ""
    return diff_html

# print(parse_json(get_json_response(get_json_URL(test_case_id,test_case_rev))))

# difference(test_case_id, test_case_rev)