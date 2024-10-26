import json
import os
from typing import Any, Mapping, Optional, Tuple

from dagster import AssetKey, MetadataValue, OpExecutionContext, Output
from dagster_dbt import (
    DagsterDbtTranslator,
    DagsterDbtTranslatorSettings,
    DbtCliInvocation,
    DbtCliResource,
    default_metadata_from_dbt_resource_props,
)

# all based on https://github.com/dagster-io/hooli-data-eng-pipelines/blob/master/hooli_data_eng/assets/dbt_assets.py


def build_DbtTranslator(warehouse_name: str, dbt_target_schema: str):  # noqa: C901
    class AsciiDbtTranslator(DagsterDbtTranslator):
        _partitioning_default_column_name = None
        _partitioning_overrides: Mapping[str, str] = {}

        def __init__(
            self,
            settings: Optional[DagsterDbtTranslatorSettings] = None,
            partitioning_default_column_name: str = "day_dt",
            partitioning_overrides: Mapping[str, str] = {},
        ):
            super().__init__(settings=settings)
            self._partitioning_default_column_name = partitioning_default_column_name
            self._partitioning_overrides = partitioning_overrides

        # for details see:
        # https://github.com/dagster-io/hooli-data-eng-pipelines/blob/master/hooli_data_eng/assets/dbt_assets.py
        def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> AssetKey:  # type: ignore
            # take key from meta if provided otherwise build unique id
            if (
                dbt_resource_props.get("meta", {})
                .get("dagster", {})
                .get("asset_key", [])
                != []
            ):
                return super().get_asset_key(dbt_resource_props)
            else:
                model_name = dbt_resource_props["name"]
                if dbt_resource_props.get("version", None) is not None:
                    model_name = model_name + "_v" + str(dbt_resource_props["version"])
                return AssetKey(model_name).with_prefix(
                    [dbt_resource_props["database"], dbt_resource_props["schema"]]
                )

        def get_group_name(self, dbt_resource_props: Mapping[str, Any]):
            "form DBT folders as asset groups. Potentially rethink in the future"
            group_name = super().get_group_name(dbt_resource_props)
            if group_name is None:
                node_path = dbt_resource_props["path"]
                if node_path == "":
                    return "upstream"
                prefix = node_path.split(os.sep)[0] if "/" in node_path else None
                if node_path.startswith("models/source_"):
                    prefix = "RAW_DATA"
                return prefix
            else:
                return group_name

        def get_metadata(
            self, dbt_resource_props: Mapping[str, Any]
        ) -> Mapping[str, Any]:
            metadata = {"partition_expr": self._partitioning_default_column_name}

            # for any deviating partitoining name a) either load the translator with different settings
            #  or b) modify it to accept an dictionary of overrides
            for k, v in self._partitioning_overrides.items():
                if dbt_resource_props["name"] == k:
                    metadata = {"partition_expr": v}

            default_metadata = default_metadata_from_dbt_resource_props(
                dbt_resource_props
            )

            return {**default_metadata, **metadata}

    return AsciiDbtTranslator


def generate_additional_metadata_for_output(
    output: Output,
    manifest: dict,
    results_by_asset_key: dict,
    dbt_resource_props_by_asset_key: dict,
    dagster_dbt_translator: DagsterDbtTranslator,
) -> Mapping[str, Any]:
    # Get the unique id of the dbt node from the output
    value = output.metadata["unique_id"].value
    if not isinstance(value, str):
        raise TypeError(
            f"Expected unique_id to be a str, got {type(value)} instead. unique_id: {value}"
        )
    dbt_unique_id: str = value

    # Get the asset key from the unique id
    asset_key = dagster_dbt_translator.get_asset_key(manifest["nodes"][dbt_unique_id])

    # Retrieve the results using the asset key, and get the rows_affected.
    result = results_by_asset_key[asset_key]
    rows_affected: Optional[int] = result["adapter_response"].get("rows_affected")
    rows_affected_metadata = {"rows_affected": rows_affected} if rows_affected else {}

    # Retrieve the dbt resource props using the asset key, and get the compiled code and owner.
    node = dbt_resource_props_by_asset_key[asset_key]
    compiled_sql: Optional[str] = node.get("compiled_code")
    compiled_sql_metadata = (
        {"compiled_sql": MetadataValue.md(compiled_sql)} if compiled_sql else {}
    )

    meta_owner: Optional[str] = node.get("meta").get("owner")
    meta_owner_metadata = {"owner": meta_owner} if meta_owner else {}

    return {
        **rows_affected_metadata,
        **compiled_sql_metadata,
        **meta_owner_metadata,
    }


def prepare_dbt_files(
    dbt_cli_task: DbtCliInvocation, dagster_dbt_translator: DagsterDbtTranslator
) -> Tuple[dict, dict]:
    run_results = dbt_cli_task.get_artifact("run_results.json")
    executed_manifest = dbt_cli_task.get_artifact("manifest.json")

    results_by_asset_key = {
        dagster_dbt_translator.get_asset_key(
            executed_manifest["nodes"][result["unique_id"]]
        ): result
        for result in run_results["results"]
    }
    dbt_resource_props_by_asset_key = {
        dagster_dbt_translator.get_asset_key(node): node
        for node in executed_manifest["nodes"].values()
    }

    return results_by_asset_key, dbt_resource_props_by_asset_key


def process_dbt_assets(
    context: OpExecutionContext,
    dbt2: DbtCliResource,
    dagster_dbt_translator2: DagsterDbtTranslator,
    dbt_mode: str = "build",  # choose run or build
):
    if context.has_partition_key:
        # map partition key range to dbt vars
        (
            first_partition,
            last_partition,
        ) = context.asset_partitions_time_window_for_output(
            list(context.selected_output_names)[0]
        )
        # This assumes a single backfill is possible
        # in case of dependent operations i.e. SCD2 you must disable the single run option
        dbt_vars = {"min_date": str(first_partition), "max_date": str(last_partition)}
        dbt_args = [dbt_mode, "--vars", json.dumps(dbt_vars)]
        dbt_cli_task = dbt2.cli(dbt_args, context=context, raise_on_error=False)
    else:
        dbt_cli_task = dbt2.cli([dbt_mode], context=context, raise_on_error=False)

    dbt_events = list(dbt_cli_task.stream())

    results_by_asset_key, dbt_resource_props_by_asset_key = prepare_dbt_files(
        dbt_cli_task, dagster_dbt_translator2
    )
    for dagster_event in dbt_events:
        if isinstance(dagster_event, Output):
            metadata = generate_additional_metadata_for_output(
                output=dagster_event,
                manifest=dbt_cli_task.get_artifact("manifest.json"),
                results_by_asset_key=results_by_asset_key,
                dbt_resource_props_by_asset_key=dbt_resource_props_by_asset_key,
                dagster_dbt_translator=dagster_dbt_translator2,
            )
            context.add_output_metadata(
                metadata=metadata,
                output_name=dagster_event.output_name,
            )
        yield dagster_event
