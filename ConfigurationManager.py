from dotenv import load_dotenv
import os
from requests.auth import HTTPBasicAuth

class ConfigurationManager:
    _authentication = None
    _topdesk_url = "https://dlfseeds.topdesk.net"
    _topdesk_application_template_id = "8413C3E6-DB89-4575-87AD-04677451CF48"

    regions = {
        "GEU":      "ed5338a1-7e8d-4ef5-976a-57f0149892d9",
        "Global":   "8a266530-cfbc-4468-9db3-38da3063bec3",
        "NA":       "0fd4120a-985e-449f-bb7b-87202db6b405",
        "OCE":      "29c182c7-95ab-4f6c-bd41-ab419cce9dac",
        "SA":       "9dcef1fd-a9b1-434b-ae4e-93eeacaee944",
    }

    departments = {
        "ERP":                              "5e6d4d35-9142-4490-aa55-51929ad6c7cc",
        "Finance":                          "83e955be-18f3-4420-9ab5-42a84f10c587",
        "General":                          "72189a51-0792-4f37-a816-dd741a2f940f",
        "Grower Services":                  "913a0f55-1fe8-4bfc-a07d-6166496e5113",
        "HR":                               "5c3ac27e-1e2e-4043-ba4d-7a12ac67441f",
        "IT":                               "166b8a06-6f0e-4d9b-b71d-4c9af2931ac8",
        "Marketing Product Mgmt":           "49586c38-aab3-4c93-a6f7-fe7388140513",
        "Production\Ops":                   "fd642194-38fd-4de0-8a27-db7e1891336a",
        "R&D":                              "fffad7cd-807a-4064-9ba1-72402632e24b",
        "Sales":                            "3b35d13b-f403-46ca-968d-50602677cfc5",
        "Supply Chain and Cust Service":    "de7c1811-e562-4331-9381-5871a4310def",
    }

    def __init__(self):
        load_dotenv(override=True)

        _topdesk_username = os.getenv('TOPDESK_USERNAME')
        _topdesk_password = os.getenv('TOPDESK_PASSWORD')
        ConfigurationManager._authentication = HTTPBasicAuth(_topdesk_username, _topdesk_password)