import dagster as dg
from .dbt import virginia_dbt_assets
from .assets import get_data, combine_data, ingest_to_dwh


all_assets = [get_data, combine_data, ingest_to_dwh, virginia_dbt_assets]
all_assets_job = dg.define_asset_job(name="weekly_refresh", selection=all_assets)

weekly_update_schedule = dg.ScheduleDefinition(
    name="web_scrape_job",
    job=all_assets_job,
    cron_schedule="0 0 * * 1",  # every Monday at midnight
)