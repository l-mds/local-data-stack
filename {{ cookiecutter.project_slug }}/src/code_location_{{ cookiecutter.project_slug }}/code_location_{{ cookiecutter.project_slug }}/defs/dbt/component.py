import dagster as dg
from .resources import get_resources_for_deployment
from dagster_dbt import DbtCliResource
from dagster_dbt.asset_decorator import dbt_assets


class DbtMinimalComponent(dg.Component, dg.Model, dg.Resolvable):
    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:

        # https://docs.dagster.io/integrations/libraries/dbt/reference#loading-dbt-models-from-a-dbt-project
        # TODO update to your needs https://github.com/dagster-io/hooli-data-eng-pipelines/blob/master/hooli-data-eng/src/hooli_data_eng/defs/dbt/component.py
        from .resources import dbt_project

        @dbt_assets(manifest=dbt_project.manifest_path)
        def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
            yield from dbt.cli(["build"], context=context).stream()

        return dg.Definitions(resources=get_resources_for_deployment(), assets=[dbt_models])


@dg.component_instance
def load(context: dg.ComponentLoadContext) -> DbtMinimalComponent:
    return DbtMinimalComponent()
