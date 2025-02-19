import dagster as dg

all_assets_job = dg.define_asset_job(name="all_assets_job")

weekly_update_schedule = dg.ScheduleDefinition(
    name="web_scrape_job",
    job=all_assets_job,
    cron_schedule="0 0 * * 1",  # every Monday at midnight
)