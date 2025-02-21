from dagster import Definitions
from .schedule import weekly_update_schedule
from dagster_dbt import DbtCliResource
from .assets import get_data, combine_data, ingest_to_dwh
from .dbt import virginia_dbt_assets
from .project import virginia_elections_project


defs = Definitions(
    assets=[get_data, combine_data, ingest_to_dwh, virginia_dbt_assets],
    schedules=[weekly_update_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=virginia_elections_project),
    }
)
