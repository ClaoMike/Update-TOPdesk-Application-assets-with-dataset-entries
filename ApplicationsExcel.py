import pandas as pd

from ConfigurationManager import ConfigurationManager
from ApiService import ApiService

class ApplicationsExcel:

    def __init__(self):
        df = pd.read_excel(
            "DLF Applications.xlsx",
            sheet_name="Separated Entries",
            keep_default_na=False  # otherwise, NA will be nan
        )
        df["Region"] = df["Region"].where(df["Region"].notna(), None).ffill()

        self.df = df

    def get_entries_where_name_is(self, name: str):
        return self.df.loc[self.df["name"] == name] # match the rows where Name matches the input

    def generate_entries(self, name: str):
        entries = []
        rows = self.get_entries_where_name_is(name=name)

        for _, row in rows.iterrows():
            region = row["Region"]
            department = row["Department"]

            region_id = ConfigurationManager.regions[region]
            department_id = ConfigurationManager.departments[department]

            # create the dataset entry asset
            print(f"      Generating entry asset for {region} & {department}")
            dataset_entry = ApiService.create_dataset_asset(region=region_id, department=department_id)
            dataset_entry_id = dataset_entry.get('data').get('unid') # extract its id
            print(f"      Entry generated: {dataset_entry_id}")
            entries.append(dataset_entry_id)

        return entries