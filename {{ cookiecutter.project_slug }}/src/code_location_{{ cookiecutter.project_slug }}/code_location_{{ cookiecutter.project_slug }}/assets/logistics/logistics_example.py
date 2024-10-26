from dagster import asset
from dagster_dbt import get_asset_key_for_model

from ..dbt_assets import unpartitioned_assets


@asset(
    compute_kind="python",
    group_name="logistics",
    deps=[get_asset_key_for_model([unpartitioned_assets], "my_first_dbt_model")],
)
def logistics_example():
    return 1
