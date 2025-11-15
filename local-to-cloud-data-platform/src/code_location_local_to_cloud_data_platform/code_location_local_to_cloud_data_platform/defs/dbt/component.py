import dagster as dg
from pathlib import Path
from .resources import get_resources_for_deployment
from dagster_dbt import DbtCliResource
from dagster_dbt.asset_decorator import dbt_assets


class DbtMinimalComponent(dg.Component, dg.Model, dg.Resolvable):
    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:

        # https://docs.dagster.io/integrations/libraries/dbt/reference#loading-dbt-models-from-a-dbt-project
        # TODO update to your needs https://github.com/dagster-io/hooli-data-eng-pipelines/blob/master/hooli-data-eng/src/hooli_data_eng/defs/dbt/component.py
        from .resources import dbt_project

        # If the dbt manifest isn't present (e.g. running unit tests without a built
        # dbt project), skip registering dbt assets so the repo can be loaded.
        manifest_path = Path(dbt_project.manifest_path)
        if not manifest_path.exists():
            dg.get_dagster_logger().warning(
                f"DBT manifest not found at {manifest_path!s}; skipping dbt assets registration."
            )
            return dg.Definitions(resources=get_resources_for_deployment(), assets=[])

        # Validate manifest is parseable JSON before passing to dbt_assets.
        try:
            import json

            with manifest_path.open("r", encoding="utf-8") as f:
                json.load(f)
        except Exception as exc:  # noqa: BLE001 - broad catch to allow test-time robustness
            dg.get_dagster_logger().warning(
                f"DBT manifest at {manifest_path!s} is not valid JSON ({exc!s}); skipping dbt assets registration."
            )
            return dg.Definitions(resources=get_resources_for_deployment(), assets=[])

        @dbt_assets(manifest=dbt_project.manifest_path)
        def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
            yield from dbt.cli(["build"], context=context).stream()

        return dg.Definitions(resources=get_resources_for_deployment(), assets=[dbt_models])


@dg.component_instance
def load(context: dg.ComponentLoadContext) -> DbtMinimalComponent:
    return DbtMinimalComponent()

