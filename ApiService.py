import requests

from ConfigurationManager import ConfigurationManager

class ApiService:
    _base_assets_url = ""

    def __init__(self):
        _base_assets_url = f"{ConfigurationManager._topdesk_url}/tas/api/assetmgmt/assets"

    @staticmethod
    def create_dataset_asset(region: str, department: str):
        url = f"{ApiService._base_assets_url}"
        headers = {"Content-Type": "application/json"}
        body = {
            "type_id": "ADA514D3-4684-43C4-8F9B-8E1DC1473F2E",
            "region": region,
            "department": department
        }

        response = requests.post(url, headers=headers, auth=ConfigurationManager._authentication, json=body)

        # --- Handle response ---
        if response.status_code >= 200 and response.status_code < 300:
            return response.json()
        else:
            raise Exception(f"status: {response.status_code}, error: {response.text}")

    @staticmethod
    def get_asset(id: str):
        url = f"{ApiService._base_assets_url}/{id}"
        headers = {"Content-Type": "application/json"}

        response = requests.get(url, headers=headers, auth=ConfigurationManager._authentication)

        # --- Handle response ---
        if response.status_code >= 200 and response.status_code < 300:
            return response.json()
        else:
            raise Exception(f"status: {response.status_code}, error: {response.text}")

    @staticmethod
    def get_assets_by_template_id(id: str):
        url = f"{ApiService._base_assets_url}/templateId/{id}"
        headers = {"Content-Type": "application/json"}

        response = requests.get(url, headers=headers, auth=ConfigurationManager._authentication)

        # --- Handle response ---
        if response.status_code >= 200 and response.status_code < 300:
            return response.json()
        else:
            raise Exception(f"status: {response.status_code}, error: {response.text}")

    @staticmethod
    def update_asset(asset_id: str, entries: list):
        url = f"{ApiService._base_assets_url}/{asset_id}"
        headers = {"Content-Type": "application/json"}
        body = {"@gridwidgetfield_8ff5051b-f8d3-4911-8302-4d99f742a959": entries}

        response = requests.post(url, headers=headers, auth=ConfigurationManager._authentication, json=body)

        # --- Handle response ---
        if response.status_code >= 200 and response.status_code < 300:
            return response.json()
        else:
            raise Exception(f"status: {response.status_code}, error: {response.text}")