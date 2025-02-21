from pathlib import Path

from dagster_dbt import DbtProject

virginia_elections_project = DbtProject(
    project_dir='C:\\Users\\muhammad.fahmi\\upwork\\virginia-elections-pipeline\\dbt'
)
virginia_elections_project.prepare_if_dev()