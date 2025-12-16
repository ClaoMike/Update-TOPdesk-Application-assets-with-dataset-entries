import pandas as pd
import requests
from dotenv import load_dotenv
import os
from requests.auth import HTTPBasicAuth

load_dotenv(override=True)
_topdesk_username = os.getenv('TOPDESK_USERNAME')
_topdesk_password = os.getenv('TOPDESK_PASSWORD')
_authentication = HTTPBasicAuth(_topdesk_username, _topdesk_password)

_topdesk_url = "https://dlfseeds.topdesk.net"
_topdesk_application_template_id = "8413C3E6-DB89-4575-87AD-04677451CF48"

regions = {
    "GEU":    "",
    "Global": "8a266530-cfbc-4468-9db3-38da3063bec3",
    "NA":     "0fd4120a-985e-449f-bb7b-87202db6b405",
    "OCE":    "29c182c7-95ab-4f6c-bd41-ab419cce9dac",
    "SA":     "9dcef1fd-a9b1-434b-ae4e-93eeacaee944",
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

def get_assets_by_template_id(id: str):
    url = f"{_topdesk_url}/tas/api/assetmgmt/assets/templateId/{id}"
    headers = { "Content-Type": "application/json" }

    response = requests.get(url, headers=headers, auth=_authentication)

    # --- Handle response ---
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()
    else:
        raise Exception(f"status: {response.status_code}, error: {response.text}")


def get_asset(id: str):
    url = f"{_topdesk_url}/tas/api/assetmgmt/assets/{id}"
    headers = { "Content-Type": "application/json" }

    response = requests.get(url, headers=headers, auth=_authentication)

    # --- Handle response ---
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()
    else:
        raise Exception(f"status: {response.status_code}, error: {response.text}")

def create_dataset_asset(region: str, department: str):
    url = f"{_topdesk_url}/tas/api/assetmgmt/assets"
    headers = { "Content-Type": "application/json" }
    body = {
        "type_id": "ADA514D3-4684-43C4-8F9B-8E1DC1473F2E",
        "region": region,
        "department": department
    }

    response = requests.post(url, headers=headers, auth=_authentication, json=body)

    # --- Handle response ---
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()
    else:
        raise Exception(f"status: {response.status_code}, error: {response.text}")

def update_asset(asset_id: str, entries: list):
    url = f"{_topdesk_url}/tas/api/assetmgmt/assets/{asset_id}"
    headers = { "Content-Type": "application/json" }
    body = { "@gridwidgetfield_8ff5051b-f8d3-4911-8302-4d99f742a959": entries }

    response = requests.post(url, headers=headers, auth=_authentication, json=body)

    # --- Handle response ---
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()
    else:
        raise Exception(f"status: {response.status_code}, error: {response.text}")

# Read a specific sheet
df = pd.read_excel(
    "DLF Applications.xlsx",
    sheet_name="Separated Entries",
    keep_default_na=False # otherwise, NA will be nan
)
df["Region"] = df["Region"].where(df["Region"].notna(), None).ffill()
print(df["Region"].unique())

application_assets = get_assets_by_template_id(id=_topdesk_application_template_id).get('results')
for asset in application_assets:
    asset_id = asset['id']

    detailed_asset = get_asset(id=asset_id)
    app_id = detailed_asset.get("data").get('name')

    entries = []
    rows = df.loc[df["Name"] == app_id]

    print("Matched rows:", len(rows))
    print(rows[["Name", "Region", "Department"]].to_string(index=False))
    print("Raw Region values repr:", [repr(x) for x in rows["Region"].tolist()])

    for _, row in rows.iterrows():
        region = row["Region"]
        department = row["Department"]

        print(f"Asset id: {asset_id}")
        print(f"App id: {app_id}")
        print(region)
        region_id = regions[region]
        department_id = departments[department]

        dataset_entry = create_dataset_asset(region=region_id, department=department_id)
        dataset_entry_id = dataset_entry.get('data').get('unid')
        entries.append(dataset_entry_id)

    _ = update_asset(asset_id=asset_id, entries=entries)


        # print(f"Region: {region} Department: {department}")
        # print(f"Dataset entry id: {dataset_entry_id}")