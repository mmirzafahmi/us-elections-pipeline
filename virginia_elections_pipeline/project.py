import os

from dagster_dbt import DbtProject

virginia_elections_project = DbtProject(
    project_dir=f'{os.getcwd()}\\virginia-elections-pipeline\\dbt'
)
virginia_elections_project.prepare_if_dev()