### load imports #######################################################################################################
from ApiService import ApiService
from ConfigurationManager import ConfigurationManager
from ApplicationsExcel import ApplicationsExcel

### load entities ######################################################################################################
config = ConfigurationManager()
api = ApiService()
apps = ApplicationsExcel()

### retrieve all assets (ids) ##########################################################################################
application_assets = ApiService.get_assets_by_template_id(id=ConfigurationManager._topdesk_application_template_id).get('results')

for asset in application_assets:
    asset_id = asset['id'] # extract id

    detailed_asset = ApiService.get_asset(id=asset_id) # fetch the full asset
    app_id = detailed_asset.get("data").get('name') # extract the app-id

    entries = apps.generate_entries(name=app_id) # get the new dataset entries
    _ = ApiService.update_asset(asset_id=asset_id, entries=entries) # update the assets with the new entries