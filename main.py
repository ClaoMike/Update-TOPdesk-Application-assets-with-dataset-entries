### load imports #######################################################################################################
print("Loading libraries ...")
from ApiService import ApiService
from ConfigurationManager import ConfigurationManager
from ApplicationsExcel import ApplicationsExcel
print("Libraries loaded :)\n")

### load entities ######################################################################################################
print("Load entities ...")
config = ConfigurationManager()
api = ApiService()
apps = ApplicationsExcel()
print("Entities loaded :)")

### retrieve all assets (ids) ##########################################################################################
print("Fetching all the existing assets and their ids ...\n")
assets_ids = [x["id"] for x in ApiService.get_assets_by_template_id(
    id=ConfigurationManager._topdesk_application_template_id).get('results')
              ]
print(f"Assets fetched: {assets_ids}\n")

for id in assets_ids:
    print(f"Updating Asset with id {id}...")
    print(f"   Fetching full asset data ...")
    detailed_asset = ApiService.get_asset(id=id) # fetch the full asset
    print(f"   Full asset data: {detailed_asset}")
    app_id = detailed_asset.get("data").get('name') # extract the app-id
    print(f"   App ID: {app_id}")

    print(f"   Generating new dataset entries as assets ...")
    entries = apps.generate_entries(name=app_id) # get the new dataset entries
    print(f"   Generated entries: {entries}")
    print(f"   Assigning new entries ...")
    _ = ApiService.update_asset(asset_id=id, entries=entries) # update the assets with the new entries
    print(f"   Entries assigned :) \n")

print(f"Assets updated :)")
########################################################################################################################