from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator
from .project import virginia_elections_project
from typing import Any, Optional
from collections.abc import Mapping

class CustomDagsterDbtTranslator(DagsterDbtTranslator):
        def get_group_name(
            self, dbt_resource_props: Mapping[str, Any]
        ) -> Optional[str]:
            return "DWH"


@dbt_assets(manifest=virginia_elections_project.manifest_path, 
            dagster_dbt_translator=CustomDagsterDbtTranslator())
def virginia_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()