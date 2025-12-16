import pandas as pd
import requests

from ConfigurationManager import ConfigurationManager

config = ConfigurationManager()

def get_assets_by_template_id(id: str):
    url = f"{config._topdesk_url}/tas/api/assetmgmt/assets/templateId/{id}"
    headers = { "Content-Type": "application/json" }

    response = requests.get(url, headers=headers, auth=config._authentication)

    # --- Handle response ---
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()
    else:
        raise Exception(f"status: {response.status_code}, error: {response.text}")


def get_asset(id: str):
    url = f"{config._topdesk_url}/tas/api/assetmgmt/assets/{id}"
    headers = { "Content-Type": "application/json" }

    response = requests.get(url, headers=headers, auth=config._authentication)

    # --- Handle response ---
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()
    else:
        raise Exception(f"status: {response.status_code}, error: {response.text}")

def create_dataset_asset(region: str, department: str):
    url = f"{config._topdesk_url}/tas/api/assetmgmt/assets"
    headers = { "Content-Type": "application/json" }
    body = {
        "type_id": "ADA514D3-4684-43C4-8F9B-8E1DC1473F2E",
        "region": region,
        "department": department
    }

    response = requests.post(url, headers=headers, auth=config._authentication, json=body)

    # --- Handle response ---
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()
    else:
        raise Exception(f"status: {response.status_code}, error: {response.text}")

def update_asset(asset_id: str, entries: list):
    url = f"{config._topdesk_url}/tas/api/assetmgmt/assets/{asset_id}"
    headers = { "Content-Type": "application/json" }
    body = { "@gridwidgetfield_8ff5051b-f8d3-4911-8302-4d99f742a959": entries }

    response = requests.post(url, headers=headers, auth=config._authentication, json=body)

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

application_assets = get_assets_by_template_id(id=config._topdesk_application_template_id).get('results')
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
        region_id = config.regions[region]
        department_id = config.departments[department]

        dataset_entry = create_dataset_asset(region=region_id, department=department_id)
        dataset_entry_id = dataset_entry.get('data').get('unid')
        entries.append(dataset_entry_id)

    _ = update_asset(asset_id=asset_id, entries=entries)