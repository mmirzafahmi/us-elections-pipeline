from dagster import Definitions, load_assets_from_modules
from virginia_elections_pipeline import assets
from virginia_elections_pipeline.schedule import weekly_update_schedule


all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,

)
