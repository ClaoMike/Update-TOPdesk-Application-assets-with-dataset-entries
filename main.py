import pandas as pd

from ApiService import ApiService
from ConfigurationManager import ConfigurationManager

config = ConfigurationManager()
api = ApiService()


# Read a specific sheet
df = pd.read_excel(
    "DLF Applications.xlsx",
    sheet_name="Separated Entries",
    keep_default_na=False # otherwise, NA will be nan
)
df["Region"] = df["Region"].where(df["Region"].notna(), None).ffill()
print(df["Region"].unique())

application_assets = ApiService.get_assets_by_template_id(id=config._topdesk_application_template_id).get('results')
for asset in application_assets:
    asset_id = asset['id']

    detailed_asset = ApiService.get_asset(id=asset_id)
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

        dataset_entry = ApiService.create_dataset_asset(region=region_id, department=department_id)
        dataset_entry_id = dataset_entry.get('data').get('unid')
        entries.append(dataset_entry_id)

    _ = ApiService.update_asset(asset_id=asset_id, entries=entries)